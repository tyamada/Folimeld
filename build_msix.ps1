[CmdletBinding()]
param(
    [ValidateSet("x64", "arm64")]
    [string]$Architecture = "x64",
    [string]$IdentityName = "Folimeld.Dev",
    [string]$Publisher = "CN=Takuma Yamada",
    [string]$PublisherDisplayName = "Takuma Yamada",
    [switch]$SkipExeBuild
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$StageRoot = Join-Path $ProjectRoot "build\msix\$Architecture"
$OutputDirectory = Join-Path $ProjectRoot "dist"

if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python was not found: $PythonExe"
}

if (-not $SkipExeBuild) {
    & (Join-Path $ProjectRoot "build_exe.bat")
    if ($LASTEXITCODE -ne 0) { throw "The Windows executable build failed." }
}

$Executable = Join-Path $OutputDirectory "Folimeld.exe"
if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
    throw "Executable was not found: $Executable"
}

$BuildMachine = & $PythonExe -c "import platform, struct; print(platform.machine().lower(), struct.calcsize('P') * 8)"
$ExpectedMachine = if ($Architecture -eq "x64") { "^(amd64|x86_64) 64$" } else { "^(arm64|aarch64) 64$" }
if ($LASTEXITCODE -ne 0 -or $BuildMachine -notmatch $ExpectedMachine) {
    throw "The Python/PyInstaller environment does not match ${Architecture}: $BuildMachine"
}

$Version = & $PythonExe -c "from folimeld import __version__; p=__version__.split('.'); print('.'.join((p + ['0'] * 4)[:4]))"
if ($LASTEXITCODE -ne 0 -or $Version -notmatch '^\d+\.\d+\.\d+\.\d+$') {
    throw "The app version cannot be converted to an MSIX version: $Version"
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

function Escape-Xml([string]$Value) {
    return [System.Security.SecurityElement]::Escape($Value)
}

$Manifest = Get-Content -Raw -Encoding UTF8 (Join-Path $ProjectRoot "packaging\msix\AppxManifest.xml.in")
$Manifest = $Manifest.Replace("@IDENTITY_NAME@", (Escape-Xml $IdentityName))
$Manifest = $Manifest.Replace("@PUBLISHER@", (Escape-Xml $Publisher))
$Manifest = $Manifest.Replace("@PUBLISHER_DISPLAY_NAME@", (Escape-Xml $PublisherDisplayName))
$Manifest = $Manifest.Replace("@VERSION@", $Version)
$Manifest = $Manifest.Replace("@ARCHITECTURE@", $Architecture)
[System.IO.File]::WriteAllText((Join-Path $ResolvedStage "AppxManifest.xml"), $Manifest, [System.Text.UTF8Encoding]::new($false))

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

Write-Host ""
Write-Host "Built unsigned $Architecture package: $OutputPackage"
Write-Host "Identity: $IdentityName"
Write-Host "Publisher: $Publisher"
Write-Host "Use the exact Partner Center identity values for Store submission."
