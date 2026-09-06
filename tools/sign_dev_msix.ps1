[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PackagePath
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Package = (Resolve-Path -LiteralPath $PackagePath).Path
if ([IO.Path]::GetExtension($Package) -ne '.msix') { throw 'Specify an MSIX package.' }

Add-Type -AssemblyName System.IO.Compression.FileSystem
$Archive = [IO.Compression.ZipFile]::OpenRead($Package)
try {
    $Entry = $Archive.GetEntry('AppxManifest.xml')
    if (-not $Entry) { throw 'AppxManifest.xml was not found.' }
    $Reader = [IO.StreamReader]::new($Entry.Open())
    try { [xml]$Manifest = $Reader.ReadToEnd() } finally { $Reader.Dispose() }
    $Publisher = [string]$Manifest.Package.Identity.Publisher
} finally { $Archive.Dispose() }
if (-not $Publisher) { throw 'The manifest Publisher is empty.' }

$ToolArchitecture = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { 'arm64' } else { 'x64' }
$SignTool = Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin" -Recurse -Filter signtool.exe -File |
    Where-Object { $_.Directory.Name -eq $ToolArchitecture } |
    Sort-Object FullName -Descending | Select-Object -First 1
if (-not $SignTool) { throw 'Install the Windows SDK signing tools first.' }

$OutputDirectory = Join-Path $ProjectRoot 'build\dev-signing'
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$CertificatePath = Join-Path $OutputDirectory 'Folimeld-dev.cer'
$ThumbprintPath = Join-Path $OutputDirectory 'thumbprint.txt'
$Certificate = $null
if (Test-Path -LiteralPath $ThumbprintPath) {
    $Thumbprint = (Get-Content -LiteralPath $ThumbprintPath -Raw).Trim()
    if ($Thumbprint -notmatch '^[0-9A-Fa-f]{40}$') { throw 'Invalid saved certificate thumbprint.' }
    $Certificate = Get-Item -LiteralPath "Cert:\CurrentUser\My\$Thumbprint" -ErrorAction SilentlyContinue
}
if ($Certificate -and ($Certificate.Subject -ne $Publisher -or
        $Certificate.NotAfter -le (Get-Date) -or -not $Certificate.HasPrivateKey)) {
    throw 'Saved certificate does not match this package or is expired. Review build/dev-signing/thumbprint.txt.'
}
if (-not $Certificate) {
    $Certificate = New-SelfSignedCertificate -Type Custom -Subject $Publisher `
        -FriendlyName 'Folimeld local MSIX development' -KeyUsage DigitalSignature `
        -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 -KeyExportPolicy NonExportable `
        -CertStoreLocation 'Cert:\CurrentUser\My' -NotAfter (Get-Date).AddYears(1) `
        -TextExtension @('2.5.29.37={text}1.3.6.1.5.5.7.3.3', '2.5.29.19={text}')
    Set-Content -LiteralPath $ThumbprintPath -Value $Certificate.Thumbprint -Encoding ASCII
}
Export-Certificate -Cert $Certificate -FilePath $CertificatePath -Force | Out-Null
$SignedPackage = Join-Path $OutputDirectory ([IO.Path]::GetFileNameWithoutExtension($Package) + '.dev-signed.msix')
if ($Package -eq $SignedPackage) { throw 'Select the original unsigned package, not the signed output.' }
Copy-Item -LiteralPath $Package -Destination $SignedPackage -Force
& $SignTool.FullName sign /fd SHA256 /s My /sha1 $Certificate.Thumbprint $SignedPackage
if ($LASTEXITCODE -ne 0) { throw "Signing failed: $LASTEXITCODE" }
$Signature = Get-AuthenticodeSignature -LiteralPath $SignedPackage
if (-not $Signature.SignerCertificate -or $Signature.SignerCertificate.Thumbprint -ne $Certificate.Thumbprint) {
    throw 'The output does not contain the expected signer certificate.'
}
Write-Host "Signed package: $SignedPackage"
Write-Host "Public certificate: $CertificatePath"
Write-Host "Thumbprint: $($Certificate.Thumbprint)"
Write-Host 'The certificate has NOT been added to Trusted People.'
Write-Host 'After checking this certificate, import its CER into LocalMachine\TrustedPeople from an administrator PowerShell.'
