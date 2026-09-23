# SelCal Windows check: locked environment, full test suite, file workflow, cross-platform replay.
#
# Run from the repository root in PowerShell (Python 3.11, 3.12 or 3.13 from python.org on PATH):
#   powershell -ExecutionPolicy Bypass -File scripts\windows_check.ps1
# Optional PyPI mirror (for slow connections):
#   powershell -ExecutionPolicy Bypass -File scripts\windows_check.ps1 -Index https://pypi.tuna.tsinghua.edu.cn/simple
#
# Writes windows_check_results\ and windows_check_results.zip. Nothing outside the repository
# folder is changed except pip's download cache.

param(
    [string]$Python = "python",
    [string]$Index = ""
)

$ErrorActionPreference = "Continue"
$root = (Get-Location).Path
$out = Join-Path $root "windows_check_results"
if (Test-Path $out) { Remove-Item -Recurse -Force $out }
New-Item -ItemType Directory -Path $out | Out-Null
$log = Join-Path $out "steps.log"

function Step([string]$name, [scriptblock]$body) {
    "=== $name" | Tee-Object -FilePath $log -Append
    & $body 2>&1 | Tee-Object -FilePath $log -Append
    "--- exit $LASTEXITCODE" | Tee-Object -FilePath $log -Append
}

$indexArgs = @()
if ($Index) { $indexArgs = @("-i", $Index) }
$venv = Join-Path $root ".venv-windows-check"
$py = Join-Path $venv "Scripts\python.exe"
$selcal = Join-Path $venv "Scripts\selcal.exe"

Step "python" { & $Python -c "import sys, platform; print(sys.version); print(platform.platform())" }
Step "create venv" { & $Python -m venv --clear $venv }
Step "install uv (only used to export the lock)" { & $py -m pip install -q @indexArgs uv }
Step "export locked requirements" {
    & $py -m uv export --locked --all-extras --no-hashes --no-emit-project -o (Join-Path $out "requirements.txt")
}
Step "install locked requirements" {
    & $py -m pip install -q @indexArgs -r (Join-Path $out "requirements.txt")
}
Step "install selcal" { & $py -m pip install -q --no-deps -e . }
Step "environment" {
    & $py -c "import sys, platform, numpy, selcal; print('python', sys.version.split()[0]); print('platform', platform.platform(), platform.machine()); print('numpy', numpy.__version__); print('selcal', selcal.__version__); numpy.show_config()"
}

Step "full test suite" {
    & $py -m pytest -q -p no:cacheprovider -rfE "--junitxml=$(Join-Path $out 'pytest.xml')" 2>&1 |
        Tee-Object -FilePath (Join-Path $out "pytest.txt")
}

$work = Join-Path $out "workflow"
New-Item -ItemType Directory -Path $work | Out-Null
Copy-Item examples\workflow\series.csv, examples\workflow\pearson.json $work
$exact = Get-Content (Join-Path $work "pearson.json") -Raw | ConvertFrom-Json
$exact.plan.null_name = "circular_shift_exact_v1"
$exact.plan.replicates = 99
$exact | ConvertTo-Json -Depth 10 | Set-Content -Encoding ascii (Join-Path $work "exact.json")
Push-Location $work
foreach ($name in @("pearson", "exact")) {
    Step "workflow $name" {
        & $selcal validate series.csv "$name.json"
        & $selcal run series.csv "$name.json" "win_$name.sqlite" --max-bytes 1048576
        & $selcal verify "win_$name.sqlite" --max-bytes 1048576
        & $selcal verify "win_$name.sqlite" --max-bytes 1048576 --replay
        & $selcal verify "win_$name.sqlite" --max-bytes 1048576 --replay-decision
        & $selcal report "win_$name.sqlite" "win_$name.html" --max-bytes 1048576
        & $selcal doctor
    }
}
$records = Join-Path $root "docs\status\evidence\windows_check\records"
if (Test-Path $records) {
    Get-ChildItem $records -Filter *.sqlite | ForEach-Object {
        Copy-Item $_.FullName $work
        Step "replay record made elsewhere: $($_.Name)" {
            & $selcal verify $_.Name --max-bytes 1048576 --replay
            & $selcal verify $_.Name --max-bytes 1048576 --replay-decision
        }
    }
}
Pop-Location

$zip = Join-Path $root "windows_check_results.zip"
if (Test-Path $zip) { Remove-Item -Force $zip }
Compress-Archive -Path (Join-Path $out "*") -DestinationPath $zip
"Done. Send back: $zip"
