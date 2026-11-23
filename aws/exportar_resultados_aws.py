from pyspark.sql import SparkSession
import csv
import os

spark = SparkSession.builder.appName("ATBD_Exportar_Resultados_AWS").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

salida = "/tmp/atbd_resultados_csv"
os.makedirs(salida, exist_ok=True)

for numero in range(1, 11):
    identificador = f"{numero:02d}"
    ruta = f"hdfs:///atbd/home_credit/results/consulta_{identificador}"
    destino = f"{salida}/consulta_{identificador}.csv"

    df = spark.read.parquet(ruta)

    if os.path.exists(destino):
        raise RuntimeError(f"El archivo ya existe: {destino}")

    with open(destino, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(df.columns)

        for fila in df.toLocalIterator():
            escritor.writerow(list(fila))

    print(f"CONSULTA {identificador} EXPORTADA: {destino}", flush=True)

spark.stop()
