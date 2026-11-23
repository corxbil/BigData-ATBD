from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Consulta_06")
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

# Seleccionar registros validos
datos = (
    df.select(
        "SK_ID_CURR",
        "TARGET",
        "AMT_ANNUITY",
        "AMT_INCOME_TOTAL",
        "CNT_FAM_MEMBERS"
    )
    .filter(
        F.col("TARGET").isin(0, 1) &
        F.col("AMT_ANNUITY").isNotNull() &
        F.col("AMT_INCOME_TOTAL").isNotNull() &
        F.col("CNT_FAM_MEMBERS").isNotNull() &
        (F.col("AMT_INCOME_TOTAL") > 0) &
        (F.col("CNT_FAM_MEMBERS") > 0)
    )
)

# Calcular ingresos anuales estimados por miembro
datos = datos.withColumn(
    "ingresos_por_miembro",
    F.col("AMT_INCOME_TOTAL") / F.col("CNT_FAM_MEMBERS")
)

# Calcular carga financiera familiar estimada
# AMT_ANNUITY es la cuota anual del credito en Home Credit
datos = datos.withColumn(
    "carga_financiera",
    F.col("AMT_ANNUITY") / F.col("ingresos_por_miembro")
)

# Crear niveles de carga financiera
datos = datos.withColumn(
    "nivel_carga",
    F.when(F.col("carga_financiera") < 0.20, "Menos del 20%")
     .when(F.col("carga_financiera") < 0.40, "20%-39%")
     .when(F.col("carga_financiera") < 0.60, "40%-59%")
     .when(F.col("carga_financiera") < 0.80, "60%-79%")
     .otherwise("80% o mas")
)

# Calcular tasa de impago por nivel de carga
resultado = (
    datos.groupBy("nivel_carga")
    .agg(
        F.count("*").alias("total_clientes"),
        F.sum("TARGET").alias("clientes_impago"),
        F.round(
            F.avg("TARGET") * 100, 2
        ).alias("tasa_impago_pct")
    )
    .orderBy("nivel_carga")
)

print("=== CONSULTA 06: CARGA FINANCIERA FAMILIAR E IMPAGO ===")
resultado.show(20, truncate=False)

# Guardar resultado en HDFS
resultado.write.mode("overwrite").parquet(
    "hdfs:///atbd/home_credit/results/consulta_06"
)

print("Resultado de consulta 06 guardado en HDFS.")

spark.stop()
