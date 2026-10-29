[CmdletBinding()]
param(
    [ValidateSet("x64", "arm64")]
    [string]$Architecture = "x64",
    [string]$IdentityName = "Folimeld.Dev",
    [string]$Publisher = "CN=Takuma Yamada",
    [string]$PublisherDisplayName = "Takuma Yamada",
    [switch]$SkipExeBuild,
    [switch]$Store,
    [string]$StoreConfig,
    [string]$PackageVersion,
    [string]$PreviousPackage,
    [switch]$ValidateOnly,
    [string]$PythonExecutable
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if ($PythonExecutable) { $PythonExe = (Resolve-Path -LiteralPath $PythonExecutable).ProviderPath }
$StageRoot = Join-Path $ProjectRoot "build\msix\$Architecture"
$OutputDirectory = Join-Path $ProjectRoot "dist"

if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python was not found: $PythonExe"
}

if ($Store -and -not $StoreConfig) {
    throw 'Store builds require -StoreConfig with verified MSIX identity values from Partner Center.'
}
if (-not $Store -and $StoreConfig) { throw '-StoreConfig requires -Store.' }
if ($Store -and (@('IdentityName', 'Publisher', 'PublisherDisplayName', 'PackageVersion') |
        Where-Object { $PSBoundParameters.ContainsKey($_) })) {
    throw 'Store builds read identity and version only from -StoreConfig.'
}

$Channel = if ($Store) { 'store' } else { 'development' }
$PreflightRoot = Join-Path $ProjectRoot "build\msix-preflight\$Channel\$Architecture"
$ConfigurationArguments = @('--architecture', $Architecture)
if ($Store) {
    $ResolvedStoreConfig = (Resolve-Path -LiteralPath $StoreConfig).ProviderPath
    $ConfigurationArguments += @('--store', '--store-config', $ResolvedStoreConfig)
} else {
    $ConfigurationArguments += @('--identity-name', $IdentityName, '--publisher', $Publisher,
                                 '--publisher-display-name', $PublisherDisplayName)
    if ($PackageVersion) { $ConfigurationArguments += @('--package-version', $PackageVersion) }
}
if ($PreviousPackage) {
    $ConfigurationArguments += @('--previous-package', (Resolve-Path -LiteralPath $PreviousPackage).ProviderPath)
}
Push-Location -LiteralPath $ProjectRoot
try {
    & $PythonExe -m tools.msix_preflight prepare @ConfigurationArguments --output-directory $PreflightRoot
    if ($LASTEXITCODE -ne 0) { throw 'MSIX configuration validation failed; no executable was rebuilt.' }
} finally { Pop-Location }
$Configuration = Get-Content -LiteralPath (Join-Path $PreflightRoot 'config.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$Version = [string]$Configuration.package_version
if ($ValidateOnly) {
    Write-Host "Configuration and manifest validated: $PreflightRoot"
    Write-Host 'This does not verify Partner Center registration, WACK, or installed-app behavior.'
    return
}

$BuildMachine = & $PythonExe -c "import platform, struct; print(platform.machine().lower(), struct.calcsize('P') * 8)"
$ExpectedMachine = if ($Architecture -eq "x64") { "^(amd64|x86_64) 64$" } else { "^(arm64|aarch64) 64$" }
if ($LASTEXITCODE -ne 0 -or $BuildMachine -notmatch $ExpectedMachine) {
    throw "The Python/PyInstaller environment does not match ${Architecture}: $BuildMachine"
}

if (-not $SkipExeBuild) {
    & (Join-Path $ProjectRoot "build_exe.bat") $PythonExe
    if ($LASTEXITCODE -ne 0) { throw "The Windows executable build failed." }
}

$Executable = Join-Path $OutputDirectory "Folimeld.exe"
if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
    throw "Executable was not found: $Executable"
}

$ResolvedStageParent = [System.IO.Path]::GetFullPath((Join-Path $ProjectRoot "build\msix"))
$ResolvedStage = [System.IO.Path]::GetFullPath($StageRoot)
if (-not $ResolvedStage.StartsWith($ResolvedStageParent + [System.IO.Path]::DirectorySeparatorChar)) {
    throw "Unexpected staging path: $ResolvedStage"
}
if (Test-Path -LiteralPath $ResolvedStage) {
    Remove-Item -LiteralPath $ResolvedStage -Recurse -Force
}
New-Item -ItemType Directory -Path (Join-Path $ResolvedStage "Assets") -Force | Out-Null

Copy-Item -LiteralPath $Executable -Destination (Join-Path $ResolvedStage "Folimeld.exe")
Copy-Item -LiteralPath (Join-Path $ProjectRoot "LICENSE") -Destination (Join-Path $ResolvedStage "LICENSE.txt")

$MsixAssets = Join-Path $ProjectRoot "packaging\msix\Assets"
if (-not (Test-Path -LiteralPath $MsixAssets -PathType Container)) {
    throw "MSIX assets were not generated: $MsixAssets"
}
Copy-Item -Path (Join-Path $MsixAssets "*.png") -Destination (Join-Path $ResolvedStage "Assets")

Copy-Item -LiteralPath (Join-Path $PreflightRoot 'AppxManifest.xml') -Destination (Join-Path $ResolvedStage 'AppxManifest.xml')

$ToolArchitecture = if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { "arm64" } else { "x64" }
$MakeAppx = Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin" -Recurse -Filter MakeAppx.exe -File |
    Where-Object { $_.Directory.Name -eq $ToolArchitecture } |
    Sort-Object FullName -Descending |
    Select-Object -First 1
if (-not $MakeAppx) {
    throw "MakeAppx.exe was not found. Install the Windows SDK."
}

$OutputPackage = Join-Path $OutputDirectory "Folimeld_${Version}_${Architecture}.msix"
& $MakeAppx.FullName pack /o /h SHA256 /d $ResolvedStage /p $OutputPackage
if ($LASTEXITCODE -ne 0) { throw "MakeAppx failed with exit code $LASTEXITCODE." }
Push-Location -LiteralPath $ProjectRoot
try {
    & $PythonExe -m tools.msix_preflight check @ConfigurationArguments --package $OutputPackage --output-directory $PreflightRoot
    if ($LASTEXITCODE -ne 0) { throw 'The generated MSIX failed static checks.' }
} finally { Pop-Location }
& $PythonExe (Join-Path $ProjectRoot "tools\source_bundle.py") --executable $Executable --artifact $OutputPackage --source-dir (Join-Path $ProjectRoot "dist\source")
if ($LASTEXITCODE -ne 0) { throw "Source association failed. Rebuild the executable and package." }

Write-Host ""
Write-Host "Built unsigned $Architecture package: $OutputPackage"
Write-Host "Channel: $Channel"
Write-Host "Identity: $($Configuration.identity_name)"
Write-Host "Publisher: $($Configuration.publisher)"
Write-Host "Use the exact Partner Center identity values for Store submission."
