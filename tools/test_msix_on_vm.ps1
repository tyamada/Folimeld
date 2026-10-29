[CmdletBinding()]
param([ValidateSet('Install','Inspect','Launch','Remove')][string]$Action='Inspect')
$ErrorActionPreference = 'Stop'
$Bundle = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'bundle.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($Bundle.identity_name -ne 'Folimeld.Dev' -or $Bundle.publisher -ne 'CN=Takuma Yamada') { throw 'Unexpected development identity.' }
$Package = Join-Path $PSScriptRoot 'Folimeld-test.msix'
$PublicCertificate = Join-Path $PSScriptRoot 'test-certificate.cer'
if ((Get-FileHash -LiteralPath $Package -Algorithm SHA256).Hash -ne $Bundle.package_sha256 -or
    (Get-FileHash -LiteralPath $PublicCertificate -Algorithm SHA256).Hash -ne $Bundle.certificate_sha256) { throw 'Bundle checksum mismatch.' }
$Certificate = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new($PublicCertificate)
if ($Certificate.Thumbprint -ne $Bundle.certificate_thumbprint -or $Certificate.Subject -ne $Bundle.publisher) { throw 'Certificate identity mismatch.' }
$StateFile = Join-Path $PSScriptRoot 'test-state.json'
$CurrentSid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
function Save-State { $script:State | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $StateFile -Encoding UTF8 }
function Require-Admin {
    $Principal = [System.Security.Principal.WindowsPrincipal]::new([System.Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $Principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)) { throw 'Use an elevated PowerShell on the test PC/VM.' }
}
$Existing = @(Get-AppxPackage -Name $Bundle.identity_name)
if ($Action -eq 'Install') {
    Require-Admin
    if (Test-Path -LiteralPath $StateFile) { throw 'Existing test state: inspect/remove it before starting another run.' }
    if ($Existing.Count) { throw 'An existing Folimeld.Dev registration was found; it will not be replaced.' }
    if ($Certificate.NotAfter -lt (Get-Date)) { throw 'Test certificate expired; prepare a fresh bundle.' }
    $TrustPath = 'Cert:\LocalMachine\TrustedPeople\' + $Certificate.Thumbprint
    $State = [ordered]@{ machine=$env:COMPUTERNAME; user_sid=$CurrentSid; certificate_thumbprint=$Certificate.Thumbprint
        package_sha256=$Bundle.package_sha256; trust_added=(-not (Test-Path -LiteralPath $TrustPath))
        package_full_name=$null; status='installation-started'; installed_utc=$null }
    Save-State
    # Persist cleanup ownership before changing the store, including failed installs.
    if ($State.trust_added) { Import-Certificate -FilePath $PublicCertificate -CertStoreLocation 'Cert:\LocalMachine\TrustedPeople' | Out-Null }
    Add-AppxPackage -Path $Package
    $Installed = Get-AppxPackage -Name $Bundle.identity_name
    if (-not $Installed -or $Installed.Publisher -ne $Bundle.publisher -or [string]$Installed.Version -ne $Bundle.version) { throw 'Installed identity does not match the bundle.' }
    $State.package_full_name=$Installed.PackageFullName
    $State.status='installed'; $State.installed_utc=[DateTime]::UtcNow.ToString('o'); Save-State
}
if ($Action -in @('Install','Inspect')) {
    $Installed = @(Get-AppxPackage -Name $Bundle.identity_name | Select-Object Name,Publisher,Version,PackageFullName,PackageFamilyName,InstallLocation,Status)
    [ordered]@{ checked_utc=[DateTime]::UtcNow.ToString('o'); machine=$env:COMPUTERNAME; user_sid=$CurrentSid
        os_version=[Environment]::OSVersion.Version.ToString(); powershell=$PSVersionTable.PSVersion.ToString()
        package_sha256=$Bundle.package_sha256; installed=$Installed
        gui_acceptance_tests='NOT RUN'; WACK='NOT RUN' } | ConvertTo-Json -Depth 6 |
        Set-Content -LiteralPath (Join-Path $PSScriptRoot 'installation-report.json') -Encoding UTF8
    $Installed | Format-List
}
if ($Action -eq 'Launch') {
    if ($Existing.Count -ne 1 -or $Existing[0].Publisher -ne $Bundle.publisher) { throw 'Expected installed development package not found.' }
    Start-Process -FilePath explorer.exe -ArgumentList ('shell:AppsFolder\' + $Existing[0].PackageFamilyName + '!Folimeld')
}
if ($Action -eq 'Remove') {
    Require-Admin
    $State = Get-Content -LiteralPath $StateFile -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($State.machine -ne $env:COMPUTERNAME -or $State.user_sid -ne $CurrentSid -or
        $State.certificate_thumbprint -ne $Certificate.Thumbprint -or $State.package_sha256 -ne $Bundle.package_sha256) { throw 'Cleanup ownership mismatch.' }
    foreach ($Installed in $Existing) {
        if ($Installed.Publisher -ne $Bundle.publisher -or [string]$Installed.Version -ne $Bundle.version -or
            ($State.package_full_name -and $Installed.PackageFullName -ne $State.package_full_name)) { throw 'A different installation is present; refusing cleanup.' }
        Remove-AppxPackage -Package $Installed.PackageFullName
    }
    if ($State.trust_added) {
        $TrustPath = 'Cert:\LocalMachine\TrustedPeople\' + $Certificate.Thumbprint
        if (Test-Path -LiteralPath $TrustPath) { Remove-Item -LiteralPath $TrustPath }
    }
    $State.status='removed'; Save-State
    Write-Host 'Removed this test package and its newly added certificate trust. Reports and user PDFs are preserved.'
}
