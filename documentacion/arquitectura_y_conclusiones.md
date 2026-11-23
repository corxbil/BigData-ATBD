# Arquitectura, metodología y conclusiones

## Arquitectura distribuida

El proyecto BigData-ATBD se ha implementado inicialmente en un entorno
local basado en Docker y posteriormente se ha desplegado en AWS Academy.

La arquitectura de AWS utiliza cinco instancias EC2 t3.medium,
con dos vCPU y 4 GiB de memoria RAM cada una.

Cada instancia ejecuta un único contenedor Docker:

| Nodo | Servicios principales |
|---|---|
| Master | Hadoop NameNode y YARN ResourceManager |
| Worker1 | HDFS DataNode y YARN NodeManager |
| Worker2 | HDFS DataNode y YARN NodeManager |
| Worker3 | HDFS DataNode y YARN NodeManager |
| Client | Apache Spark y herramientas Hadoop |

La comunicación entre nodos utiliza las direcciones IP privadas
de AWS dentro de la misma red virtual.

## Configuración del almacenamiento HDFS

HDFS distribuye los archivos CSV entre tres DataNodes y utiliza
un factor de replicación de tres.

El conjunto de datos Home Credit contiene diez archivos CSV,
con un tamaño conjunto de aproximadamente 2,5 GiB.

La comprobación mediante hdfs fsck confirmó:

- Estado del sistema: HEALTHY.
- Total de archivos: 10.
- Bloques validados: 27.
- Replicación media: 3.
- Bloques perdidos: 0.
- Bloques corruptos: 0.
- Bloques infrarreplicados: 0.

## Procesamiento con YARN y Spark

El ResourceManager coordina los recursos de tres NodeManagers.

Las pruebas realizadas confirmaron que los tres nodos se
registraron en estado RUNNING.

Apache Spark 3.5.6 se ejecutó desde el contenedor cliente
utilizando YARN como gestor de recursos.

Se realizó una prueba distribuida de cálculo de Pi y se
comprobó la lectura de application_train.csv desde HDFS.

El archivo contiene 307511 registros y 122 columnas.

Posteriormente se ejecutaron diez consultas de análisis
de riesgo crediticio y se almacenaron sus resultados
en formato Parquet dentro de HDFS.

## Validación de los resultados

Los resultados Parquet se exportaron a diez archivos CSV
para su comprobación en Windows.

Los valores obtenidos se contrastaron con las diez
visualizaciones realizadas mediante Python y Matplotlib.

Las diez gráficas coincidieron con los resultados
calculados en AWS, sin diferencias numéricas detectadas.

## Conclusiones

El proyecto demuestra que es posible desplegar una arquitectura
de almacenamiento y procesamiento distribuido utilizando
Docker, Hadoop, YARN y Spark sobre instancias EC2 independientes.

La replicación triple de HDFS proporciona redundancia de
almacenamiento, y YARN permite gestionar los recursos
disponibles para las aplicaciones Spark.

Las diez consultas analíticas permitieron estudiar diferentes
factores relacionados con el riesgo crediticio utilizando
datos reales del conjunto Home Credit.

La coincidencia de los resultados entre el entorno local
y AWS valida la reproducibilidad de los análisis realizados.

Como limitación, el entorno AWS Academy utiliza recursos
temporales y máquinas con memoria limitada, por lo que
las aplicaciones se ejecutaron con configuraciones moderadas
de memoria y número de ejecutores.