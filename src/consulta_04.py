from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_04")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

ruta = "hdfs:///atbd/home_credit/raw/application_train.csv"

# Leer datos desde HDFS
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(ruta)
)

# Seleccionar columnas necesarias
datos = (
    df.select(
        "SK_ID_CURR",
        "TARGET",
        "NAME_EDUCATION_TYPE",
        "AMT_INCOME_TOTAL"
    )
    .filter(
        F.col("TARGET").isin(0, 1) &
        F.col("NAME_EDUCATION_TYPE").isNotNull() &
        F.col("AMT_INCOME_TOTAL").isNotNull() &
        (F.col("AMT_INCOME_TOTAL") >= 0)
    )
)

# Clasificar los ingresos
datos = datos.withColumn(
    "rango_ingresos",
    F.when(F.col("AMT_INCOME_TOTAL") < 100000, "Menos de 100.000")
     .when(F.col("AMT_INCOME_TOTAL") < 200000, "100.000-199.999")
     .when(F.col("AMT_INCOME_TOTAL") < 300000, "200.000-299.999")
     .otherwise("300.000 o mas")
)

# Calcular tasa de impago por educación e ingresos
resultado = (
    datos.groupBy(
        "NAME_EDUCATION_TYPE",
        "rango_ingresos"
    )
    .agg(
        F.count("*").alias("total_clientes"),
        F.sum("TARGET").alias("clientes_impago"),
        F.round(
            F.avg("TARGET") * 100, 2
        ).alias("tasa_impago_pct")
    )
    .orderBy(
        "NAME_EDUCATION_TYPE",
        "rango_ingresos"
    )
)

print("=== CONSULTA 04: EDUCACION, INGRESOS E IMPAGO ===")
resultado.show(50, truncate=False)

# Guardar resultados en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_04"
)

print("Resultado de consulta 04 guardado en HDFS.")

spark.stop()
