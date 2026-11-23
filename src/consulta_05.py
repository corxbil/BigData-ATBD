from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_05")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

base = "hdfs:///atbd/home_credit/raw/"

# Tabla principal
app = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(base + "application_train.csv")
    .select("SK_ID_CURR", "TARGET")
    .filter(F.col("TARGET").isin(0, 1))
)

# Solicitudes previas
prev = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(base + "previous_application.csv")
    .select("SK_ID_CURR", "SK_ID_PREV")
)

# Número de solicitudes previas por cliente
prev_por_cliente = (
    prev.groupBy("SK_ID_CURR")
    .agg(F.countDistinct("SK_ID_PREV").alias("num_solicitudes_previas"))
)

# Join con la tabla principal
datos = (
    app.join(prev_por_cliente, "SK_ID_CURR", "left")
    .withColumn(
        "num_solicitudes_previas",
        F.coalesce(F.col("num_solicitudes_previas"), F.lit(0))
    )
)

# Agrupar en rangos
datos = datos.withColumn(
    "grupo_solicitudes_previas",
    F.when(F.col("num_solicitudes_previas") == 0, "0")
     .when(F.col("num_solicitudes_previas") == 1, "1")
     .when(F.col("num_solicitudes_previas").between(2, 3), "2-3")
     .when(F.col("num_solicitudes_previas").between(4, 6), "4-6")
     .otherwise("7 o mas")
)

# Resultado final
resultado = (
    datos.groupBy("grupo_solicitudes_previas")
    .agg(
        F.count("*").alias("total_clientes"),
        F.sum("TARGET").alias("clientes_impago"),
        F.round(F.avg("TARGET") * 100, 2).alias("tasa_impago_pct")
    )
    .orderBy("grupo_solicitudes_previas")
)

print("=== CONSULTA 05: SOLICITUDES PREVIAS E IMPAGO ===")
resultado.show(20, truncate=False)

# Guardar en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_05"
)

print("Resultado de consulta 05 guardado en HDFS.")

spark.stop()