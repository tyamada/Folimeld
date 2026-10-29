[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Package,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [string]$SourceDirectory
)
$ErrorActionPreference = 'Stop'
if (-not $SourceDirectory) { $SourceDirectory = Join-Path (Split-Path -Parent $PSScriptRoot) 'dist/source' }
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.Security
$InputPackage = (Resolve-Path -LiteralPath $Package).ProviderPath
$Archive = [System.IO.Compression.ZipFile]::OpenRead($InputPackage)
try {
    $Reader = [System.IO.StreamReader]::new($Archive.GetEntry('AppxManifest.xml').Open())
    try { [xml]$Manifest = $Reader.ReadToEnd() } finally { $Reader.Dispose() }
    $HashAlgorithm = [System.Security.Cryptography.SHA256]::Create()
    $ExecutableStream = $Archive.GetEntry('Folimeld.exe').Open()
    try { $ExecutableHash = [BitConverter]::ToString($HashAlgorithm.ComputeHash($ExecutableStream)).Replace('-','').ToLowerInvariant() }
    finally { $ExecutableStream.Dispose(); $HashAlgorithm.Dispose() }
} finally { $Archive.Dispose() }
$Identity = $Manifest.Package.Identity
if ($Identity.Name -ne 'Folimeld.Dev' -or $Identity.Publisher -ne 'CN=Takuma Yamada' -or $Identity.ProcessorArchitecture -ne 'x64') {
    throw 'Only the Folimeld.Dev x64 development identity is supported.'
}
$Destination = [System.IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $Destination) { throw 'Choose a new output directory; existing bundles are preserved.' }
$InputHash = (Get-FileHash -LiteralPath $InputPackage -Algorithm SHA256).Hash.ToLowerInvariant()
$SourceRecord = Get-Content -LiteralPath (Join-Path $SourceDirectory ((Split-Path -Leaf $InputPackage) + '-' + $InputHash + '.json')) -Raw -Encoding UTF8 | ConvertFrom-Json
if ($SourceRecord.artifact_sha256 -ne $InputHash -or $SourceRecord.executable_sha256 -ne $ExecutableHash -or
    $SourceRecord.source_archive -notmatch '^Folimeld-source-[0-9a-f]{64}\.zip$') { throw 'Input source association mismatch.' }
$SourceArchive = Join-Path $SourceDirectory $SourceRecord.source_archive
if ((Get-FileHash -LiteralPath $SourceArchive -Algorithm SHA256).Hash -ne $SourceRecord.source_sha256) { throw 'Source ZIP hash mismatch.' }
$SignTool = Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin" -Filter signtool.exe -Recurse -File |
    Where-Object { $_.Directory.Name -eq 'x64' } | Sort-Object FullName -Descending | Select-Object -First 1
if (-not $SignTool) { throw 'Install the Windows SDK signing tools on the build computer.' }
New-Item -ItemType Directory -Path $Destination | Out-Null
$Signed = Join-Path $Destination 'Folimeld-test.msix'
Copy-Item -LiteralPath $InputPackage -Destination $Signed
$PrivateKeyFile = Join-Path $Destination 'temporary-signing-key.pfx'
$Rsa = [System.Security.Cryptography.RSACng]::new(2048)
$Certificate = $null
try {
    $Request = [System.Security.Cryptography.X509Certificates.CertificateRequest]::new(
        [string]$Identity.Publisher, $Rsa, [System.Security.Cryptography.HashAlgorithmName]::SHA256,
        [System.Security.Cryptography.RSASignaturePadding]::Pkcs1)
    $Request.CertificateExtensions.Add([System.Security.Cryptography.X509Certificates.X509BasicConstraintsExtension]::new($false,$false,0,$true))
    $Request.CertificateExtensions.Add([System.Security.Cryptography.X509Certificates.X509KeyUsageExtension]::new(
        [System.Security.Cryptography.X509Certificates.X509KeyUsageFlags]::DigitalSignature,$true))
    $Oids = [System.Security.Cryptography.OidCollection]::new()
    [void]$Oids.Add([System.Security.Cryptography.Oid]::new('1.3.6.1.5.5.7.3.3'))
    $Request.CertificateExtensions.Add([System.Security.Cryptography.X509Certificates.X509EnhancedKeyUsageExtension]::new($Oids,$true))
    $Certificate = $Request.CreateSelfSigned([DateTimeOffset]::UtcNow.AddMinutes(-10),[DateTimeOffset]::UtcNow.AddDays(7))
    $PfxPassword = [Guid]::NewGuid().ToString('N')
    [System.IO.File]::WriteAllBytes($PrivateKeyFile,$Certificate.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Pfx,$PfxPassword))
    & $SignTool.FullName sign /fd SHA256 /f $PrivateKeyFile /p $PfxPassword $Signed
    if ($LASTEXITCODE -ne 0) { throw 'Development package signing failed.' }
    [System.IO.File]::WriteAllBytes((Join-Path $Destination 'test-certificate.cer'),$Certificate.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert))
    $Signature = Get-AuthenticodeSignature -LiteralPath $Signed
    if (-not $Signature.SignerCertificate -or $Signature.SignerCertificate.Thumbprint -ne $Certificate.Thumbprint) {
        throw 'The signed package certificate does not match the generated certificate.'
    }
    $SignedArchive = [System.IO.Compression.ZipFile]::OpenRead($Signed)
    $HashAlgorithm = [System.Security.Cryptography.SHA256]::Create()
    $ExecutableStream = $SignedArchive.GetEntry('Folimeld.exe').Open()
    try { $SignedExecutableHash = [BitConverter]::ToString($HashAlgorithm.ComputeHash($ExecutableStream)).Replace('-','').ToLowerInvariant() }
    finally { $ExecutableStream.Dispose(); $HashAlgorithm.Dispose(); $SignedArchive.Dispose() }
    if ($SignedExecutableHash -ne $ExecutableHash) { throw 'Signing changed the executable payload.' }
    $SignedArchive = [System.IO.Compression.ZipFile]::OpenRead($Signed)
    $SignatureStream = $SignedArchive.GetEntry('AppxSignature.p7x').Open()
    $SignatureMemory = [System.IO.MemoryStream]::new()
    try { $SignatureStream.CopyTo($SignatureMemory); $SignatureBytes = $SignatureMemory.ToArray() }
    finally { $SignatureStream.Dispose(); $SignatureMemory.Dispose(); $SignedArchive.Dispose() }
    if ([System.Text.Encoding]::ASCII.GetString($SignatureBytes,0,4) -ne 'PKCX') { throw 'Unexpected MSIX signature header.' }
    $Cms = [System.Security.Cryptography.Pkcs.SignedCms]::new()
    $Cms.Decode([byte[]]$SignatureBytes[4..($SignatureBytes.Length-1)])
    $Cms.CheckSignature($true) # Cryptographic signature only; does not add certificate trust.
    if ($Cms.SignerInfos.Count -ne 1 -or $Cms.SignerInfos[0].Certificate.Thumbprint -ne $Certificate.Thumbprint) { throw 'CMS signer mismatch.' }
    Copy-Item -LiteralPath $SourceArchive -Destination $Destination
    $SourceRecord.artifact = 'Folimeld-test.msix'
    $SourceRecord.artifact_sha256 = (Get-FileHash -LiteralPath $Signed -Algorithm SHA256).Hash.ToLowerInvariant()
    $SourceRecord.association = 'Original source association verified against unsigned and signed package executable hashes.'
    $SourceRecord | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $Destination 'artifact-source.json') -Encoding UTF8
    $Record = [ordered]@{
        package='Folimeld-test.msix'; package_sha256=(Get-FileHash -LiteralPath $Signed -Algorithm SHA256).Hash
        unsigned_package_sha256=(Get-FileHash -LiteralPath $InputPackage -Algorithm SHA256).Hash
        identity_name=[string]$Identity.Name; publisher=[string]$Identity.Publisher
        version=[string]$Identity.Version; architecture=[string]$Identity.ProcessorArchitecture
        certificate_sha256=(Get-FileHash -LiteralPath (Join-Path $Destination 'test-certificate.cer') -Algorithm SHA256).Hash
        certificate_thumbprint=$Certificate.Thumbprint; certificate_expires_utc=$Certificate.NotAfter.ToUniversalTime().ToString('o')
        signature_status_on_build_machine=[string]$Signature.Status
        cms_signature_verified_without_trust=$true
        purpose='Seven-day development test certificate; no certificate-store changes on build computer. Not for Store submission.'
        installation='NOT RUN'; acceptance_tests='NOT RUN'; WACK='NOT RUN'
    }
    $Record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Destination 'bundle.json') -Encoding UTF8
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'test_msix_on_vm.ps1') -Destination $Destination
    Write-Host "Prepared test bundle: $Destination"
} finally {
    if (Test-Path -LiteralPath $PrivateKeyFile) { Remove-Item -LiteralPath $PrivateKeyFile -Force }
    if ($Certificate) { $Certificate.Dispose() }
    $Rsa.Dispose()
}
