Write-Host "`n=== CONTENEDORES DOCKER ==="
docker ps --format "table {{.Names}}\t{{.Status}}"

Write-Host "`n=== ESTADO HDFS ==="
docker exec atbd-master hdfs dfsadmin -report

Write-Host "`n=== ESTADO YARN ==="
docker exec atbd-master yarn node -list
