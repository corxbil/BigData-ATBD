from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_01")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

ruta = "hdfs:///atbd/home_credit/raw/application_train.csv"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(ruta)
)

# Seleccionar los datos necesarios
datos = df.select(
    "SK_ID_CURR",
    "TARGET",
    "DAYS_BIRTH",
    "CODE_GENDER"
)

# Calcular edad aproximada
datos = datos.withColumn(
    "edad",
    F.floor(-F.col("DAYS_BIRTH") / 365.25)
)

# Crear rangos de edad
datos = datos.withColumn(
    "rango_edad",
    F.when(F.col("edad") < 30, "Menos de 30")
     .when(F.col("edad") < 40, "30-39")
     .when(F.col("edad") < 50, "40-49")
     .when(F.col("edad") < 60, "50-59")
     .otherwise("60 o más")
)

# Filtrar registros válidos
datos = datos.filter(
    F.col("TARGET").isin(0, 1) &
    F.col("CODE_GENDER").isin("M", "F") &
    F.col("edad").between(18, 100)
)

# Calcular tasa de impago
resultado = (
    datos.groupBy("rango_edad", "CODE_GENDER")
    .agg(
        F.count("*").alias("total_clientes"),
        F.sum("TARGET").alias("clientes_impago"),
        F.round(F.avg("TARGET") * 100, 2).alias("tasa_impago_pct")
    )
    .orderBy("rango_edad", "CODE_GENDER")
)

print("=== CONSULTA 01: IMPAGO POR EDAD Y GENERO ===")
resultado.show(50, truncate=False)

# Guardar resultado en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_01"
)

print("Resultado guardado correctamente en HDFS.")

spark.stop()
