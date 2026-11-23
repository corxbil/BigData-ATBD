from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_02")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

base = "hdfs:///atbd/home_credit/raw/"

# Leer tabla principal
app = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(base + "application_train.csv")
    .select("SK_ID_CURR", "TARGET")
)

# Leer historial de créditos externos
bureau = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(base + "bureau.csv")
    .select(
        "SK_ID_CURR",
        "CREDIT_ACTIVE",
        "AMT_CREDIT_SUM_DEBT"
    )
)

# Sumar la deuda de créditos activos por cliente
deuda_cliente = (
    bureau
    .filter(F.col("CREDIT_ACTIVE") == "Active")
    .groupBy("SK_ID_CURR")
    .agg(
        F.sum(
            F.coalesce(F.col("AMT_CREDIT_SUM_DEBT"), F.lit(0))
        ).alias("deuda_externa")
    )
)

# Relacionar deuda externa con los clientes
datos = (
    app.join(deuda_cliente, "SK_ID_CURR", "left")
    .withColumn(
        "deuda_externa",
        F.coalesce(F.col("deuda_externa"), F.lit(0))
    )
    .filter(F.col("TARGET").isin(0, 1))
)

# Clasificar por nivel de deuda
datos = datos.withColumn(
    "nivel_deuda",
    F.when(F.col("deuda_externa") <= 0, "Sin deuda registrada")
     .when(F.col("deuda_externa") < 100000, "Menos de 100.000")
     .when(F.col("deuda_externa") < 500000, "100.000-499.999")
     .when(F.col("deuda_externa") < 1000000, "500.000-999.999")
     .otherwise("1.000.000 o más")
)

# Calcular indicadores
resultado = (
    datos.groupBy("nivel_deuda")
    .agg(
        F.count("*").alias("total_clientes"),
        F.sum("TARGET").alias("clientes_impago"),
        F.round(
            F.avg("TARGET") * 100, 2
        ).alias("tasa_impago_pct")
    )
    .orderBy("nivel_deuda")
)

print("=== CONSULTA 02: DEUDA EXTERNA E IMPAGO ===")
resultado.show(20, truncate=False)

# Guardar resultados en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_02"
)

print("Resultado de consulta 02 guardado en HDFS.")

spark.stop()
