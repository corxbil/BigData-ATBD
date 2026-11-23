from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("ATBD_Lectura_Home_Credit")
    .getOrCreate()
)

ruta = "hdfs:///atbd/home_credit/raw/application_train.csv"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(ruta)
)

print("=== ESQUEMA DEL DATASET ===")
df.printSchema()

print("=== NUMERO DE REGISTROS ===")
print(df.count())

print("=== PRIMEROS 5 REGISTROS ===")
df.select(
    "SK_ID_CURR",
    "TARGET",
    "CODE_GENDER",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT"
).show(5, truncate=False)

spark.stop()
