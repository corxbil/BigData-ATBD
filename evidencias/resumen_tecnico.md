# BigData-ATBD - Resumen tecnico de AWS

## Arquitectura
- Plataforma: AWS Academy, region us-east-1.
- Cinco instancias EC2 t3.medium.
- Un contenedor Docker por instancia.
- Master: NameNode y ResourceManager.
- Tres workers: DataNode y NodeManager.
- Cliente: Apache Spark 3.5.6.
- Comunicacion mediante direcciones IP privadas de AWS.

## Almacenamiento
- Hadoop HDFS distribuido.
- Tres DataNodes activos.
- Factor de replicacion: 3.
- Diez datasets CSV del conjunto Home Credit.
- 27 bloques validados.
- Estado HDFS: HEALTHY.
- Bloques perdidos: 0.
- Bloques corruptos: 0.
- Bloques infrarreplicados: 0.

## Procesamiento
- YARN con tres NodeManagers en estado RUNNING.
- PySpark ejecutado desde la instancia cliente.
- Prueba distribuida de calculo de Pi completada.
- Lectura de application_train.csv validada:
  307511 registros y 122 columnas.
- Diez consultas analiticas ejecutadas correctamente.
- Diez resultados Parquet almacenados en HDFS.

## Visualizacion y validacion
- Diez resultados exportados a CSV desde AWS.
- Diez graficas PNG disponibles.
- Diez graficas contrastadas con los resultados de AWS.
- Diferencias numericas detectadas: 0.

## Evidencias
- evidencias/01_infraestructura/
- evidencias/02_hdfs/
- evidencias/03_yarn_spark/
- evidencias/04_resultados/