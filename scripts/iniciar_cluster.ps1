$ErrorActionPreference = "Stop"

# Localizar los scripts del proyecto
$rutaScripts = $PSScriptRoot

Write-Host "`n=== ATBD: INICIO DEL CLUSTER ==="

# Verificar que los cinco contenedores estan activos
$contenedores = @(
    "atbd-master",
    "atbd-worker1",
    "atbd-worker2",
    "atbd-worker3",
    "atbd-client"
)

foreach ($contenedor in $contenedores) {
    $estado = docker inspect -f '{{.State.Running}}' $contenedor 2>$null

    if ($LASTEXITCODE -ne 0 -or $estado -ne "true") {
        throw "El contenedor $contenedor no esta activo"
    }
}

Write-Host "Los cinco contenedores estan activos."

# Iniciar los servicios del master
& "$rutaScripts\iniciar_master.ps1"

if (-not $?) {
    throw "Error ejecutando iniciar_master.ps1"
}

# Iniciar los servicios de los workers
& "$rutaScripts\iniciar_workers.ps1"

if (-not $?) {
    throw "Error ejecutando iniciar_workers.ps1"
}

Write-Host "`n=== ARRANQUE DEL CLUSTER FINALIZADO ==="
