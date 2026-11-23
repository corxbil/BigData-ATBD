# PROYECTO BIGDATA-ATBD

## 1. Introducción
Análisis distribuido del conjunto de datos Home Credit mediante
Docker, Apache Hadoop, HDFS, YARN, Apache Spark y AWS Academy.

## 2. Objetivos
- Diseñar una arquitectura distribuida de cinco nodos.
- Desplegar un contenedor Docker por instancia EC2.
- Configurar almacenamiento distribuido con HDFS.
- Configurar procesamiento distribuido mediante YARN y Spark.
- Ejecutar diez consultas analíticas sobre Home Credit.
- Generar y validar diez visualizaciones.

## 3. Arquitectura del sistema
Cinco instancias EC2 t3.medium en AWS Academy:

- Master: NameNode y ResourceManager.
- Worker1: DataNode y NodeManager.
- Worker2: DataNode y NodeManager.
- Worker3: DataNode y NodeManager.
- Client: Apache Spark 3.5.6.

Cada instancia ejecuta un contenedor Docker independiente.

## 4. Configuración del clúster
### 4.1 Docker
### 4.2 Hadoop HDFS
### 4.3 YARN
### 4.4 Apache Spark
### 4.5 Comunicación entre instancias

## 5. Almacenamiento distribuido
- Diez archivos CSV del conjunto Home Credit.
- Factor de replicación HDFS: 3.
- Tres DataNodes activos.
- 27 bloques validados.
- Estado del sistema de archivos: HEALTHY.
- Cero bloques perdidos o corruptos.

## 6. Procesamiento distribuido
- Tres NodeManagers en estado RUNNING.
- Ejecución de Spark sobre YARN.
- Prueba de cálculo de Pi completada.
- Validación de application_train.csv:
  307511 registros y 122 columnas.

## 7. Consultas analíticas

### 7.01 Consulta 01. Impago por edad y género
Analiza la relación entre la edad, el género y la tasa de impago.
Utiliza application_train.csv y agrupa los clientes por rangos
de edad y género.

### 7.02 Consulta 02. Deuda externa e impago
Estudia la relación entre el endeudamiento registrado en otras
entidades y la tasa de impago. Combina información de solicitudes
con datos del historial crediticio mediante operaciones join.

### 7.03 Consulta 03. Retrasos en pagos e impago
Analiza cómo se relacionan los retrasos históricos en los pagos
con la probabilidad observada de impago. Utiliza operaciones de
agrupación y unión de datos por cliente.

### 7.04 Consulta 04. Educación, ingresos e impago
Compara las tasas de impago según el nivel educativo y el rango
de ingresos. Agrupa los clientes por ambas dimensiones.

### 7.05 Consulta 05. Solicitudes previas e impago
Estudia la relación entre el número de solicitudes crediticias
anteriores y la tasa de impago de los clientes.

### 7.06 Consulta 06. Carga financiera familiar e impago
Analiza la relación entre la carga financiera del cliente y
su tasa de impago, utilizando rangos de carga financiera.

### 7.07 Consulta 07. Utilización mensual de tarjetas
Calcula la utilización media de tarjetas de crédito durante
los doce meses anteriores, agrupando por MONTHS_BALANCE.

### 7.08 Consulta 08. Ocupación, antigüedad e impago
Compara la tasa de impago según el tipo de ocupación y la
antigüedad laboral, mediante una matriz de 18 ocupaciones
y cinco rangos de antigüedad.

### 7.09 Consulta 09. Evolución mensual de retrasos
Analiza la evolución de los registros con retrasos en los
doce meses anteriores, agrupando por MONTHS_BALANCE.

### 7.10 Consulta 10. Solicitudes no aprobadas e impago
Estudia la relación entre el número de solicitudes anteriores
rechazadas o canceladas y la tasa de impago observada.

### Ejecución y almacenamiento
Las diez consultas se ejecutaron mediante PySpark sobre YARN
en el clúster AWS de cinco instancias EC2.

Los datos de entrada se almacenaron en HDFS bajo /atbd/datasets/.

Los resultados se guardaron en formato Parquet bajo
/atbd/home_credit/results/consulta_XX.

Posteriormente se exportaron a CSV y se contrastaron con las
diez visualizaciones del proyecto, sin diferencias numéricas.

## 8. Visualización de resultados
Se generaron diez gráficas PNG utilizando Python y Matplotlib.

Los valores representados se contrastaron con los resultados
exportados del clúster AWS, sin diferencias numéricas detectadas.

## 9. Pruebas y validación
### 9.1 Infraestructura Docker
### 9.2 Integridad de HDFS
### 9.3 Funcionamiento de YARN
### 9.4 Ejecución distribuida de Spark
### 9.5 Validación de los resultados

## 10. Conclusiones

## 11. Anexos y evidencias
- evidencias/01_infraestructura/
- evidencias/02_hdfs/
- evidencias/03_yarn_spark/
- evidencias/04_resultados/
---