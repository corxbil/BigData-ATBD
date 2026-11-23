from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("ATBD_Verificar_Resultados_AWS")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

for numero in range(1, 11):
    identificador = f"{numero:02d}"
    ruta = f"hdfs:///atbd/home_credit/results/consulta_{identificador}"

    print(f"\n========== CONSULTA {identificador} ==========", flush=True)

    df = spark.read.parquet(ruta)

    print(f"Filas: {df.count()}", flush=True)
    print(f"Columnas: {', '.join(df.columns)}", flush=True)

    df.show(30, truncate=False)

spark.stop()
