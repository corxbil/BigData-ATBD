from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_10")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

base = "hdfs:///atbd/home_credit/raw/"

# Leer clientes de entrenamiento
app = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(base + "application_train.csv")
    .select("SK_ID_CURR", "TARGET")
    .filter(F.col("TARGET").isin(0, 1))
)

# Leer solicitudes anteriores
prev = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(base + "previous_application.csv")
    .select(
        "SK_ID_CURR",
        "SK_ID_PREV",
        "NAME_CONTRACT_STATUS"
    )
)

# Seleccionar solicitudes rechazadas o canceladas
prev_no_aprobadas = (
    prev.filter(
        F.col("NAME_CONTRACT_STATUS").isin(
            "Refused", "Canceled"
        )
    )
)

# Contar solicitudes rechazadas o canceladas por cliente
historial_cliente = (
    prev_no_aprobadas
    .groupBy("SK_ID_CURR")
    .agg(
        F.countDistinct("SK_ID_PREV")
        .alias("num_no_aprobadas")
    )
)

# Unir con la tabla principal
datos = (
    app.join(
        historial_cliente,
        "SK_ID_CURR",
        "left"
    )
    .withColumn(
        "num_no_aprobadas",
        F.coalesce(
            F.col("num_no_aprobadas"),
            F.lit(0)
        )
    )
)

# Clasificar clientes por historial
datos = datos.withColumn(
    "grupo_no_aprobadas",
    F.when(F.col("num_no_aprobadas") == 0, "0")
     .when(F.col("num_no_aprobadas") == 1, "1")
     .when(F.col("num_no_aprobadas").between(2, 3), "2-3")
     .when(F.col("num_no_aprobadas").between(4, 6), "4-6")
     .otherwise("7 o mas")
)

# Calcular tasa de impago
resultado = (
    datos.groupBy("grupo_no_aprobadas")
    .agg(
        F.count("*").alias("total_clientes"),
        F.sum("TARGET").alias("clientes_impago"),
        F.round(
            F.avg("TARGET") * 100, 2
        ).alias("tasa_impago_pct")
    )
    .orderBy("grupo_no_aprobadas")
)

print(
    "=== CONSULTA 10: SOLICITUDES RECHAZADAS "
    "O CANCELADAS E IMPAGO ==="
)

resultado.show(20, truncate=False)

# Guardar resultados en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_10"
)

print("Resultado de consulta 10 guardado en HDFS.")

spark.stop()
