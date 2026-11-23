$ErrorActionPreference = "Stop"

Write-Host "`n=== INICIAR SERVICIOS DEL MASTER ==="

$procesos = (docker exec atbd-master jps) -join "`n"

if ($LASTEXITCODE -ne 0) {
    throw "No se puede acceder al contenedor master"
}

if ($procesos -notmatch "\bNameNode\b") {
    Write-Host "Iniciando NameNode..."
    docker exec -d atbd-master hdfs namenode

    if ($LASTEXITCODE -ne 0) {
        throw "Error al lanzar NameNode"
    }
}
else {
    Write-Host "NameNode ya esta activo."
}

if ($procesos -notmatch "\bResourceManager\b") {
    Write-Host "Iniciando ResourceManager..."
    docker exec -d atbd-master yarn resourcemanager

    if ($LASTEXITCODE -ne 0) {
        throw "Error al lanzar ResourceManager"
    }
}
else {
    Write-Host "ResourceManager ya esta activo."
}

Write-Host "`nComprobacion de procesos:"
docker exec atbd-master jps
