from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_07")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

ruta = "hdfs:///atbd/home_credit/raw/credit_card_balance.csv"

# Leer los datos desde HDFS
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(ruta)
)

# Seleccionar y validar las columnas necesarias
datos = (
    df.select(
        "SK_ID_PREV",
        "MONTHS_BALANCE",
        "AMT_BALANCE",
        "AMT_CREDIT_LIMIT_ACTUAL"
    )
    .filter(
        F.col("MONTHS_BALANCE").isNotNull() &
        F.col("AMT_BALANCE").isNotNull() &
        F.col("AMT_CREDIT_LIMIT_ACTUAL").isNotNull() &
        (F.col("AMT_CREDIT_LIMIT_ACTUAL") > 0)
    )
)

# Calcular utilización del límite de crédito
datos = datos.withColumn(
    "utilizacion_pct",
    F.least(
        F.greatest(
            F.col("AMT_BALANCE") /
            F.col("AMT_CREDIT_LIMIT_ACTUAL") * 100,
            F.lit(0.0)
        ),
        F.lit(100.0)
    )
)

# Analizar los últimos 12 meses disponibles
datos = datos.filter(
    F.col("MONTHS_BALANCE").between(-12, -1)
)

# Agregar por mes
resultado = (
    datos.groupBy("MONTHS_BALANCE")
    .agg(
        F.count("*").alias("num_registros"),
        F.round(
            F.avg("utilizacion_pct"), 2
        ).alias("utilizacion_media_pct")
    )
    .orderBy("MONTHS_BALANCE")
)

print("=== CONSULTA 07: UTILIZACION MENSUAL DE TARJETAS ===")
resultado.show(20, truncate=False)

# Guardar resultado en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_07"
)

print("Resultado de consulta 07 guardado en HDFS.")

spark.stop()
