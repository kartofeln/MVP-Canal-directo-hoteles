# Arranque seguro del POC MICE (Windows PowerShell)
# Uso: clic derecho -> Ejecutar con PowerShell, o:  .\run_api.ps1

$Root = $PSScriptRoot
Set-Location $Root
$env:PYTHONPATH = $Root

Write-Host "Carpeta POC:" $Root
Write-Host "PYTHONPATH:" $env:PYTHONPATH
Write-Host ""

$venvPython = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: No existe .venv. Ejecuta primero:" -ForegroundColor Red
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

$env:Path = (Join-Path $Root ".venv\Scripts") + ";" + $env:Path

# Puerto: 8000 a veces da WinError 10013 (Hyper-V, reserva de Windows, otro programa).
# Cambia aquí o en sesión:  $env:POC_PORT = "8010"
if (-not $env:POC_PORT) { $env:POC_PORT = "8010" }
$port = $env:POC_PORT

Write-Host "Arrancando uvicorn en http://127.0.0.1:$port" -ForegroundColor Green
Write-Host "(Si falla, prueba otro: `$env:POC_PORT='8020'; .\run_api.ps1)" -ForegroundColor DarkGray
Write-Host "Comprueba build en: GET http://127.0.0.1:$port/meta-poc" -ForegroundColor Green
Write-Host ""

& uvicorn app.main:app --reload --host 127.0.0.1 --port $port
