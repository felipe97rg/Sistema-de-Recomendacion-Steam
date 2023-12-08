# Analisis de datos de la plataforma STEAM

Este es mi proyecto de ciencia de datos para la etapa de labs del bootcamp de soy henry donde buscaremos implementar las habilidades obtenidas durante la etape de aprendizaje.
## Descripción

Tomando el rol de cientifico de datos de la plataforma STEAM en este proyecto que tiene como objetivo crear un sistema de recomendacion de los juegos basado en los datos suministrados por la plataforma. Se llevaran acabo 3 diferentes procesos, desde la extraccion y tratamiento de los datos pasando por un analisis de los mismos hasta la implementacion del sistema de recomendacion.

## Herramientas usadas
- Visual Studio Code como editor de codigo
- Python como lenguaje de programacion
- GitHub como repositorio del proyecto
- FastAPI como framework
- Render

## Etapa de ingenieria de datos
En esta etapa de ingenieria de datos serralizop un proceso de ETL, extraccion, tratamiento y carga donde se recibieron 3 archivos JSON con informacion acerca de los videjuegos, los jugadores y las reseñas de estos.
#### Link: https://github.com/felipe97rg/proyecto_3/blob/main/ETL.ipynb
### Fuente de los datos 
https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj

## Etapa de analisis de datos
En esta etapa se realizo el EDA, analisis exploratorio de datos donde empezamos con una conversion de los datos verificanddo datos nulos, duplicados, outliers y el formato de los datos para posteriormente realizar el analisis de estos mediante garficos.
#### Link: https://github.com/felipe97rg/proyecto_3/blob/main/EDA_17.ipynb

## Sistema de recomendacion
Una vez completadas las  etapas anteriores los datos se encuentran preparados para realazar las respectivas funciones y el sistema de recomendacion los cuales podran ser consultados mediante el framework FastAPI 
#### Linkl FastAPI : https://proyecto-3-jflm.onrender.com/docs


    def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.


    def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.


    def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)


    def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)


    def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.






## Video
En el siguiente enlace podras encontrar un video con un pequeño resumen acerca del proyecto
#### Link: https://www.youtube.com/channel/UCrR9T1nEFfQpWviNudpueBw

## Requisitos

Asegúrate de tener instaladas las siguientes bibliotecas antes de ejecutar el código:

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

Puedes instalarlos usando el siguiente comando:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
