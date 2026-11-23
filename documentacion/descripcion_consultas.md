# Descripción de las diez consultas analíticas

## Consulta 01. Impago por edad y género
Analiza la relación entre la edad, el género y la tasa de impago.
Utiliza application_train.csv y agrupa los clientes por rangos
de edad y género.

## Consulta 02. Deuda externa e impago
Estudia la relación entre el endeudamiento registrado en otras
entidades y la tasa de impago. Combina información de solicitudes
con datos del historial crediticio mediante operaciones join.

## Consulta 03. Retrasos en pagos e impago
Analiza cómo se relacionan los retrasos históricos en los pagos
con la probabilidad observada de impago. Utiliza operaciones de
agrupación y unión de datos por cliente.

## Consulta 04. Educación, ingresos e impago
Compara las tasas de impago según el nivel educativo y el rango
de ingresos. Agrupa los clientes por ambas dimensiones.

## Consulta 05. Solicitudes previas e impago
Estudia la relación entre el número de solicitudes crediticias
anteriores y la tasa de impago de los clientes.

## Consulta 06. Carga financiera familiar e impago
Analiza la relación entre la carga financiera del cliente y
su tasa de impago, utilizando rangos de carga financiera.

## Consulta 07. Utilización mensual de tarjetas
Calcula la utilización media de tarjetas de crédito durante
los doce meses anteriores, agrupando por MONTHS_BALANCE.

## Consulta 08. Ocupación, antigüedad e impago
Compara la tasa de impago según el tipo de ocupación y la
antigüedad laboral, mediante una matriz de 18 ocupaciones
y cinco rangos de antigüedad.

## Consulta 09. Evolución mensual de retrasos
Analiza la evolución de los registros con retrasos en los
doce meses anteriores, agrupando por MONTHS_BALANCE.

## Consulta 10. Solicitudes no aprobadas e impago
Estudia la relación entre el número de solicitudes anteriores
rechazadas o canceladas y la tasa de impago observada.

## Ejecución y almacenamiento
Las diez consultas se ejecutaron mediante PySpark sobre YARN
en el clúster AWS de cinco instancias EC2.

Los datos de entrada se almacenaron en HDFS bajo /atbd/datasets/.

Los resultados se guardaron en formato Parquet bajo
/atbd/home_credit/results/consulta_XX.

Posteriormente se exportaron a CSV y se contrastaron con las
diez visualizaciones del proyecto, sin diferencias numéricas.