param(
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173
)

$ErrorActionPreference = "Stop"

$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$BackendDir = Join-Path $RootDir "backend"
$FrontendDir = Join-Path $RootDir "frontend"
$FrontendNodeModules = Join-Path $FrontendDir "node_modules"

if (-not (Test-Path -LiteralPath $BackendDir)) {
    throw "Backend directory not found: $BackendDir"
}

if (-not (Test-Path -LiteralPath $FrontendDir)) {
    throw "Frontend directory not found: $FrontendDir"
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not available in PATH."
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "npm is not available in PATH."
}

if (-not (Test-Path -LiteralPath $FrontendNodeModules)) {
    Write-Warning "frontend\node_modules does not exist. Run `npm install` in the frontend directory first."
}

$BackendCommand = @"
Set-Location -LiteralPath '$RootDir'
`$env:PYTHONPATH = '$BackendDir'
python -m uvicorn app.main:app --host 127.0.0.1 --port $BackendPort --reload
"@

$FrontendCommand = @"
Set-Location -LiteralPath '$FrontendDir'
`$env:VITE_API_BASE_URL = 'http://127.0.0.1:$BackendPort/api'
npm run dev -- --host 127.0.0.1 --port $FrontendPort
"@

Start-Process powershell.exe -WorkingDirectory $RootDir -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    $BackendCommand
)

Start-Sleep -Seconds 2

Start-Process powershell.exe -WorkingDirectory $FrontendDir -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    $FrontendCommand
)

Write-Host "Backend:  http://127.0.0.1:$BackendPort"
Write-Host "Frontend: http://127.0.0.1:$FrontendPort"
