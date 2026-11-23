$ErrorActionPreference = "Stop"

# Situarse en la raíz del proyecto
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "`n=== ATBD: GENERACION DE GRAFICAS ==="

for ($i = 1; $i -le 10; $i++) {

    $numero = "{0:D2}" -f $i
    $archivo = ".\src\grafico_consulta_$numero.py"

    Write-Host "`nGenerando grafica $numero..."

    python $archivo

    if ($LASTEXITCODE -ne 0) {
        throw "Error generando la grafica $numero"
    }

    Write-Host "Grafica $numero generada correctamente."
}

Write-Host "`n=== LAS 10 GRAFICAS HAN FINALIZADO ==="
