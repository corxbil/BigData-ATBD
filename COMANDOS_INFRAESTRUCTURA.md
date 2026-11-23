# ATBD — Comandos de infraestructura

**Proyecto:** BigData-ATBD · **Entorno:** Windows + AWS Academy

> Resumen de los comandos principales para montar, ejecutar y comprobar el clúster. No es un historial literal de la terminal: algunos comandos son ejemplos de reproducción. Los archivos `aws/compose/`, `aws/config/` y `scripts/` contienen la configuración utilizada.

## 1. Máquinas AWS

Creamos **5 instancias EC2 t3.medium** (2 vCPU, 4 GiB RAM) en AWS Academy:

- **Master:** NameNode y ResourceManager.
- **Worker1, Worker2 y Worker3:** DataNode y NodeManager.
- **Client:** Spark y ejecución de consultas.

Las instancias se crearon desde la interfaz de AWS Academy; no hay un comando de creación EC2 que documentar.

## 2. Preparación con Docker (Windows / PowerShell)

Las imágenes se definieron en `docker/Dockerfile`, `docker/Dockerfile.hadoop` y `docker/Dockerfile.spark`.

```powershell
docker build -t atbd-base:1.0 -f docker/Dockerfile .
docker build -t atbd-hadoop:1.0 -f docker/Dockerfile.hadoop .
docker build -t atbd-spark:1.0 -f docker/Dockerfile.spark .
docker compose -f compose.yaml up -d
docker ps
```

Para reconstruirlas se necesitan los paquetes de Hadoop 3.4.3 y Spark 3.5.6 en `docker/downloads/`, que no se incluyen en GitHub por tamaño.

## 3. Despliegue en AWS

Distribuimos las imágenes Docker a las EC2 y arrancamos **un contenedor por máquina**, utilizando los archivos de `aws/compose/`. Comandos representativos:

```powershell
# Windows: preparar imágenes para su traslado
docker save -o exports/atbd-hadoop.tar atbd-hadoop:1.0
docker save -o exports/atbd-spark.tar atbd-spark:1.0
```

```bash
# En cada EC2: cargar la imagen que corresponda (ejemplo)
docker load -i atbd-hadoop.tar

# En cada EC2: arrancar SOLO el YAML de su propio nodo (ejemplo master)
docker compose -f master.yaml up -d
docker ps
```

El cliente utiliza la imagen `atbd-spark:1.0`. Las rutas reales de archivos y volúmenes se especifican en `aws/compose/`.

## 4. Comprobaciones de Hadoop y YARN (EC2 / contenedores)

```bash
jps                      # Procesos Java del nodo
hdfs dfsadmin -report     # Estado de los DataNodes
yarn node -list -all       # Estado de los NodeManagers
hdfs fsck /atbd/datasets  # Integridad de los datos
```

**Resultado comprobado:** 3 DataNodes activos, 3 NodeManagers en `RUNNING`, 10 archivos CSV, 27 bloques validados, replicación 3 y estado `HEALTHY`.

## 5. Datos y analíticas (cliente Spark)

Los CSV de Home Credit se cargaron en HDFS bajo `/atbd/datasets/`. Ejemplos de las operaciones realizadas:

```bash
hdfs dfs -mkdir -p /atbd/datasets
hdfs dfs -put *.csv /atbd/datasets/     # Desde el directorio donde estén los CSV
hdfs dfs -ls /atbd/datasets/
```

Las **10 consultas PySpark** se ejecutaron mediante `spark-submit` con **YARN**. Ejemplo de invocación (los parámetros concretos de memoria y ejecutores se ajustaron al clúster):

```bash
spark-submit --master yarn --deploy-mode client consulta_01.py
hdfs dfs -ls /atbd/home_credit/results/
```

Código utilizado: `aws/consultas/consulta_01.py` a `consulta_10.py`.

## 6. Resultados y evidencias

Los resultados se guardaron en **Parquet en HDFS** (`/atbd/home_credit/results/`) y se exportaron después a CSV para compararlos con las gráficas locales.

- `evidencias/01_infraestructura/`: contenedores y procesos por máquina.
- `evidencias/02_hdfs/`: DataNodes e integridad del almacenamiento.
- `evidencias/03_yarn_spark/`: NodeManagers activos.
- `evidencias/04_resultados/csv_aws/`: 10 resultados exportados.
- `evidencias/04_resultados/graficas/`: 10 gráficas.

**Validación final:** las diez consultas ejecutadas en AWS coincidieron numéricamente con los resultados utilizados en local.

> **Nota:** las rutas HDFS son internas del clúster; no aparecen como carpetas de GitHub. No incluir contraseñas ni claves privadas en el repositorio.
