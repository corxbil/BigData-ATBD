$ErrorActionPreference = "Stop"

Write-Host "`n=== INICIAR SERVICIOS DE LOS WORKERS ==="

$workers = @(
    "atbd-worker1",
    "atbd-worker2",
    "atbd-worker3"
)

foreach ($worker in $workers) {

    Write-Host "`n=== $worker ==="

    $procesos = (docker exec $worker jps) -join "`n"

    if ($LASTEXITCODE -ne 0) {
        throw "No se puede acceder a $worker"
    }

    if ($procesos -notmatch "\bDataNode\b") {
        Write-Host "Iniciando DataNode..."
        docker exec -d $worker hdfs datanode

        if ($LASTEXITCODE -ne 0) {
            throw "Error al lanzar DataNode en $worker"
        }
    }
    else {
        Write-Host "DataNode ya esta activo."
    }

    if ($procesos -notmatch "\bNodeManager\b") {
        Write-Host "Iniciando NodeManager..."
        docker exec -d $worker yarn nodemanager

        if ($LASTEXITCODE -ne 0) {
            throw "Error al lanzar NodeManager en $worker"
        }
    }
    else {
        Write-Host "NodeManager ya esta activo."
    }

    Write-Host "`nProcesos actuales:"
    docker exec $worker jps
}

Write-Host "`n=== COMPROBACION FINALIZADA ==="
