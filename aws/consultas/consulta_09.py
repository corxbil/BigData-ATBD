from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_09")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

ruta = "hdfs:///atbd/datasets/bureau_balance.csv"

# Leer datos desde HDFS
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(ruta)
)

# Seleccionar los datos necesarios
datos = (
    df.select(
        "SK_ID_BUREAU",
        "MONTHS_BALANCE",
        "STATUS"
    )
    .filter(
        F.col("MONTHS_BALANCE").between(-12, -1) &
        F.col("STATUS").isin("0", "1", "2", "3", "4", "5")
    )
)

# Identificar registros con retrasos
datos = datos.withColumn(
    "tiene_retraso",
    F.when(F.col("STATUS").isin("1", "2", "3", "4", "5"), 1)
     .otherwise(0)
)

# Agrupar por mes
resultado = (
    datos.groupBy("MONTHS_BALANCE")
    .agg(
        F.count("*").alias("total_registros"),
        F.sum("tiene_retraso").alias("registros_con_retraso"),
        F.round(
            F.avg("tiene_retraso") * 100, 2
        ).alias("porcentaje_retraso")
    )
    .orderBy("MONTHS_BALANCE")
)

print("=== CONSULTA 09: EVOLUCION MENSUAL DE RETRASOS ===")
resultado.show(20, truncate=False)

# Guardar resultados en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_09"
)

print("Resultado de consulta 09 guardado en HDFS.")

spark.stop()
