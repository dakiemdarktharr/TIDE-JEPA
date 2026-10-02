param(
    [string]$Config = 'data/pilot/vi-en-ai-v4.2/tide-seed-17.json',
    [string]$Checkpoint = 'runs/vi-en-ai-v4.2/tide-seed-17/best.pt',
    [int]$Port = 8765
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$sitePackages = Join-Path $projectRoot '.venv\Lib\site-packages'
if (-not (Test-Path -LiteralPath $sitePackages -PathType Container)) {
    throw "Project runtime is missing at $sitePackages. Create .venv and install requirements-test-cpu.txt first."
}
if (-not (Test-Path -LiteralPath $Config -PathType Leaf) -or -not (Test-Path -LiteralPath $Checkpoint -PathType Leaf)) {
    throw 'Run config or checkpoint does not exist. Pass paths relative to the project root or absolute paths.'
}
if ($Port -lt 1024 -or $Port -gt 65535) { throw 'Port must be in 1024..65535.' }
$env:PYTHONPATH = $sitePackages
py -3.11 -B -c "import sys, torch; assert sys.version_info[:2] == (3, 11); assert torch.__version__ == '2.14.0+cpu'"
if ($LASTEXITCODE -ne 0) { throw 'Python 3.11 / PyTorch CPU runtime check failed.' }
py -3.11 -B -m tide_jepa.demo $Config $Checkpoint --port $Port
if ($LASTEXITCODE -ne 0) { throw "Demo exited with code $LASTEXITCODE." }
