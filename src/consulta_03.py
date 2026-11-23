from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_03")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

base = "hdfs:///atbd/home_credit/raw/"

# Leer clientes y su indicador de impago
app = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(base + "application_train.csv")
    .select("SK_ID_CURR", "TARGET")
)

# Leer el historial de pagos
pagos = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(base + "installments_payments.csv")
    .select(
        "SK_ID_CURR",
        "DAYS_INSTALMENT",
        "DAYS_ENTRY_PAYMENT"
    )
)

# Calcular días de retraso en cada pago
# Un resultado positivo significa pago posterior al vencimiento
pagos = (
    pagos.filter(
        F.col("DAYS_INSTALMENT").isNotNull() &
        F.col("DAYS_ENTRY_PAYMENT").isNotNull()
    )
    .withColumn(
        "dias_retraso",
        F.greatest(
            F.col("DAYS_ENTRY_PAYMENT") -
            F.col("DAYS_INSTALMENT"),
            F.lit(0)
        )
    )
)

# Obtener el máximo retraso registrado de cada cliente
retrasos_cliente = (
    pagos.groupBy("SK_ID_CURR")
    .agg(
        F.max("dias_retraso").alias("max_dias_retraso")
    )
)

# Unir el historial con los clientes de entrenamiento
datos = (
    app.join(retrasos_cliente, "SK_ID_CURR", "inner")
    .filter(F.col("TARGET").isin(0, 1))
)

# Clasificar clientes por máximo retraso histórico
datos = datos.withColumn(
    "nivel_retraso",
    F.when(F.col("max_dias_retraso") == 0, "Sin retrasos")
     .when(F.col("max_dias_retraso") <= 7, "1-7 dias")
     .when(F.col("max_dias_retraso") <= 30, "8-30 dias")
     .when(F.col("max_dias_retraso") <= 90, "31-90 dias")
     .otherwise("Mas de 90 dias")
)

# Calcular tasa de impago por nivel de retraso
resultado = (
    datos.groupBy("nivel_retraso")
    .agg(
        F.count("*").alias("total_clientes"),
        F.sum("TARGET").alias("clientes_impago"),
        F.round(
            F.avg("TARGET") * 100, 2
        ).alias("tasa_impago_pct")
    )
    .orderBy("nivel_retraso")
)

print("=== CONSULTA 03: RETRASOS EN PAGOS E IMPAGO ===")
resultado.show(20, truncate=False)

# Guardar resultados en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_03"
)

print("Resultado de consulta 03 guardado en HDFS.")

spark.stop()
