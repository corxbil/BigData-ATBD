from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ATBD_Validacion_CSV_AWS").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

ruta = "hdfs://master:9000/atbd/datasets/application_train.csv"

df = spark.read.option("header", "true").csv(ruta)

print("======================================")
print("VALIDACION SPARK SQL EN AWS")
print("Registros:", df.count())
print("Columnas:", len(df.columns))
print("======================================")

spark.stop()
