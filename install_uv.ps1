#requires -Version 7.2
[CmdletBinding()]
param([string]$RecordRoot)
$ErrorActionPreference = 'Stop'
$arch = [Runtime.InteropServices.RuntimeInformation]::OSArchitecture
if (-not $IsWindows -or ($arch -ne 'X64' -and $arch -ne 'Arm64')) {
    throw 'Windows x64 or ARM64 is required.'
}
$isArm64 = ($arch -eq 'Arm64')
$root = [IO.Path]::GetFullPath($PSScriptRoot)
$runtimeProfileName = if ($isArm64) { 'windows-arm64-uv-runtime.json' } else { 'windows-uv-runtime.json' }
$lockFileName = if ($isArm64) { 'requirements-windows-arm64-uv.lock' } else { 'requirements-windows-uv.lock' }
$expectedPlatform = if ($isArm64) { 'windows-arm64' } else { 'windows-x86_64' }

$profileData = Get-Content -LiteralPath (Join-Path $root $runtimeProfileName) -Raw | ConvertFrom-Json
$lockPath = Join-Path $root $lockFileName
$lockText = [IO.File]::ReadAllText($lockPath).Replace("`r`n", "`n")
$lockHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($lockText))).ToLowerInvariant()
if ($lockHash -cne $profileData.lock_sha256) { throw 'Lock hash mismatch.' }
if ($profileData.schema_version -ne 1 -or $profileData.platform -cne $expectedPlatform) { throw 'Unsupported runtime profile.' }
$runtime = Join-Path $root '.uv-runtime'
$venv = Join-Path $root '.venv'
$shortcutPath = Join-Path $root 'Folimeld UV.lnk'
$debugShortcutPath = Join-Path $root 'Folimeld UV diagnostics.lnk'
foreach ($path in @($runtime, $venv, $shortcutPath, $debugShortcutPath)) {
    if (Test-Path -LiteralPath $path) { throw "Existing installation item; use a fresh source folder: $path" }
}
$stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffffffZ') + '-' + [guid]::NewGuid().ToString('N')
$appVersion = [regex]::Match([IO.File]::ReadAllText((Join-Path $root 'folimeld/__init__.py')), '__version__\s*=\s*"([A-Za-z0-9][A-Za-z0-9.+_-]*)"').Groups[1].Value
if (-not $appVersion) { throw 'Application version is missing.' }
if (-not $RecordRoot) {
    if (-not $env:LOCALAPPDATA -or -not [IO.Path]::IsPathFullyQualified($env:LOCALAPPDATA)) { throw 'Absolute LOCALAPPDATA is required.' }
    $RecordRoot = Join-Path $env:LOCALAPPDATA ('Folimeld-UV/install-records/' + $appVersion)
}
if (-not [IO.Path]::IsPathFullyQualified($RecordRoot)) { throw 'RecordRoot must be absolute.' }
$recordDirectory = Join-Path $RecordRoot $stamp
[void](New-Item -ItemType Directory -Path $recordDirectory)
$record = [ordered]@{schema_version=1; status='started'; started_utc=$stamp; source_root=$root; lock_sha256=$lockHash; downloads=@(); commands=@(); created_shortcuts=@()}
function Save-Record {
    $record | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $recordDirectory 'installation.json') -Encoding utf8
}
function Fetch-Verified($entry, [string]$destination) {
    $uri = [uri]$entry.url
    if ($uri.Scheme -ne 'https' -or ($uri.Host -ne 'github.com' -and $uri.Host -ne 'api.nuget.org') -or $uri.UserInfo -or $uri.Query) { throw 'Unexpected download URL.' }
    if ($entry.sha256 -notmatch '^[a-f0-9]{64}$') { throw 'Invalid archive hash.' }
    Invoke-WebRequest -Uri $uri.AbsoluteUri -OutFile $destination
    $actual = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -cne $entry.sha256) { throw 'Downloaded archive hash mismatch.' }
    $record.downloads += @{url=$uri.AbsoluteUri; path=$destination; sha256=$actual; bytes=(Get-Item -LiteralPath $destination).Length}
    Save-Record
}
function Run-Recorded([string]$executable, [string[]]$arguments, [string]$logName) {
    $record.commands += @{executable=$executable; arguments=$arguments; log=$logName}
    Save-Record
    & $executable @arguments 2>&1 | Out-File -LiteralPath (Join-Path $recordDirectory $logName) -Encoding utf8
    if ($LASTEXITCODE -ne 0) { throw "Step failed; inspect $logName in $recordDirectory" }
}
Save-Record
try {
    [void](New-Item -ItemType Directory -Path $runtime)
    $downloads = Join-Path $runtime 'downloads'
    [void](New-Item -ItemType Directory -Path $downloads)
    $uvZip = Join-Path $downloads 'uv.zip'
    $pythonArchiveName = if ($isArm64) { 'python.nupkg' } else { 'python.tar.gz' }
    $pythonArchive = Join-Path $downloads $pythonArchiveName
    Fetch-Verified $profileData.uv $uvZip
    Fetch-Verified $profileData.python $pythonArchive
    $uvDirectory = Join-Path $runtime 'uv'
    Expand-Archive -LiteralPath $uvZip -DestinationPath $uvDirectory
    $uvExecutable = Join-Path $uvDirectory 'uv.exe'
    $pythonDirectory = Join-Path $runtime 'python'
    [void](New-Item -ItemType Directory -Path $pythonDirectory)
    if ($isArm64) {
        Expand-Archive -LiteralPath $pythonArchive -DestinationPath $pythonDirectory
        $pythonExecutable = Join-Path $pythonDirectory 'tools/python.exe'
        if (-not (Test-Path -LiteralPath $pythonExecutable)) { throw 'ARM64 Python executable missing after extraction.' }
    } else {
        $tar = Join-Path $env:SystemRoot 'System32/tar.exe'
        $entries = & $tar -tzf $pythonArchive
        if ($LASTEXITCODE -ne 0) { throw 'Python archive listing failed.' }
        foreach ($entry in $entries) {
            if ($entry -match '(^[/\\]|^[A-Za-z]:|(^|[/\\])\.\.([/\\]|$))') { throw 'Unsafe Python archive path.' }
        }
        Run-Recorded $tar @('-xzf', $pythonArchive, '-C', $pythonDirectory) 'python-extraction.log'
        $pythonExecutable = Join-Path $pythonDirectory 'python/python.exe'
    }
    Run-Recorded $uvExecutable @('--version') 'uv-version.log'
    if ((Get-Content -LiteralPath (Join-Path $recordDirectory 'uv-version.log') -Raw).Trim() -notmatch ('^uv ' + [regex]::Escape($profileData.uv.version) + '(\s|$)')) { throw 'uv version mismatch.' }
    $uvArguments = @('--no-config', '--no-python-downloads', '--cache-dir', (Join-Path $runtime 'cache'))
    Run-Recorded $uvExecutable ($uvArguments + @('venv', '--python', $pythonExecutable, $venv)) 'venv.log'
    $venvPython = Join-Path $venv 'Scripts/python.exe'
    Run-Recorded $uvExecutable ($uvArguments + @('pip', 'sync', '--python', $venvPython, '--require-hashes', '--only-binary', ':all:', '--index-url', 'https://pypi.org/simple', $lockPath)) 'dependency-sync.log'
    Run-Recorded $uvExecutable ($uvArguments + @('pip', 'check', '--python', $venvPython)) 'dependency-check.log'
    Push-Location -LiteralPath $root
    try {
        Run-Recorded $venvPython @('-c', 'from pathlib import Path; import launch_uv; launch_uv.validate_environment(Path.cwd()); print("Pinned environment verified; application not launched.")') 'launcher-validation.log'
        Run-Recorded $venvPython @('-c', 'import importlib.metadata as m,json,sys; print(json.dumps({"python":sys.version,"executable":sys.executable,"prefix":sys.prefix,"dependencies":{d.metadata["Name"]:d.version for d in m.distributions()}},indent=2))') 'installed-environment.json'
    } finally { Pop-Location }
    $shell = New-Object -ComObject WScript.Shell
    foreach ($item in @(@($shortcutPath, 'pythonw.exe'), @($debugShortcutPath, 'python.exe'))) {
        $shortcut = $shell.CreateShortcut($item[0])
        $shortcut.TargetPath = Join-Path $venv ('Scripts/' + $item[1])
        $shortcut.Arguments = '"' + (Join-Path $root 'launch_uv.py') + '"'
        $shortcut.WorkingDirectory = $root
        $shortcut.Description = 'Folimeld source + uv (separate settings and logs)'
        $shortcut.Save()
        $record.created_shortcuts += $item[0]
    }
    $record.status = 'installed-verified-not-launched'
    $record.completed_utc = [DateTime]::UtcNow.ToString('o')
    Save-Record
    Write-Output "Dedicated environment verified. Application not launched. Record: $recordDirectory"
} catch {
    $record.status = 'failed-preserved-for-inspection'
    $record.error = $_.Exception.Message
    Save-Record
    throw
}
