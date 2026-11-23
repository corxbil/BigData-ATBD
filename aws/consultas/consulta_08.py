from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_08")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

ruta = "hdfs:///atbd/datasets/application_train.csv"

# Leer datos desde HDFS
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(ruta)
)

# Seleccionar y validar los registros
datos = (
    df.select(
        "SK_ID_CURR",
        "TARGET",
        "DAYS_EMPLOYED",
        "OCCUPATION_TYPE"
    )
    .filter(
        F.col("TARGET").isin(0, 1) &
        F.col("DAYS_EMPLOYED").isNotNull() &
        F.col("OCCUPATION_TYPE").isNotNull() &
        (F.col("DAYS_EMPLOYED") <= 0)
    )
)

# Calcular antigüedad laboral aproximada en años
datos = datos.withColumn(
    "antiguedad_anios",
    F.floor(-F.col("DAYS_EMPLOYED") / 365.25)
)

# Clasificar antigüedad laboral
datos = datos.withColumn(
    "rango_antiguedad",
    F.when(F.col("antiguedad_anios") < 2, "Menos de 2")
     .when(F.col("antiguedad_anios") < 5, "2-4")
     .when(F.col("antiguedad_anios") < 10, "5-9")
     .when(F.col("antiguedad_anios") < 20, "10-19")
     .otherwise("20 o mas")
)

# Agregar por ocupación y antigüedad laboral
resultado = (
    datos.groupBy("OCCUPATION_TYPE", "rango_antiguedad")
    .agg(
        F.count("*").alias("total_clientes"),
        F.sum("TARGET").alias("clientes_impago"),
        F.round(
            F.avg("TARGET") * 100, 2
        ).alias("tasa_impago_pct")
    )
    .orderBy("OCCUPATION_TYPE", "rango_antiguedad")
)

print("=== CONSULTA 08: EMPLEO, OCUPACION E IMPAGO ===")
resultado.show(100, truncate=False)

# Guardar resultados en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_08"
)

print("Resultado de consulta 08 guardado en HDFS.")

spark.stop()
