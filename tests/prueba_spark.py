import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("ATBD_Prueba_3_Workers")
    .getOrCreate()
)

df = spark.range(1, 1000001, numPartitions=12)

resultado = (
    df.withColumn("grupo", F.col("id") % 2)
      .groupBy("grupo")
      .agg(F.count("*").alias("cantidad"))
      .orderBy("grupo")
)

resultado.show()

print("PRUEBA FINALIZADA. Manteniendo Spark activo para comprobar YARN...")
time.sleep(120)

spark.stop()

