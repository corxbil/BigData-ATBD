$ErrorActionPreference = "Stop"

Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "`n=== ATBD: EJECUCION DE CONSULTAS ==="

for ($i = 1; $i -le 10; $i++) {

    $numero = "{0:D2}" -f $i
    $archivo = "consulta_$numero.py"

    Write-Host "`n=== CONSULTA $numero ==="

    docker cp ".\src\$archivo" "atbd-client:/tmp/$archivo"

    if ($LASTEXITCODE -ne 0) {
        throw "Error copiando $archivo al cliente"
    }

    docker exec atbd-client spark-submit `
        --master yarn `
        --deploy-mode client `
        --num-executors 3 `
        --executor-cores 1 `
        --executor-memory 1g `
        --driver-memory 1g `
        --conf spark.driver.host=client `
        --conf spark.dynamicAllocation.enabled=false `
        "/tmp/$archivo"

    if ($LASTEXITCODE -ne 0) {
        throw "Error ejecutando la consulta $numero"
    }

    Write-Host "Consulta $numero completada correctamente."
}

Write-Host "`n=== LAS 10 CONSULTAS HAN FINALIZADO ==="
