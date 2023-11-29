from typing import Optional

from fastapi import FastAPI

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI()

df_PlayTimeGenre = pd.read_parquet("df_PlayTimeGenre.parquet")
df_UserForGenre = pd.read_parquet("df_UserForGenre.parquet")
df_UserRecommend = pd.read_parquet("df_UserRecommend.parquet")
df_UserWorstDeveloper = pd.read_parquet("df_UserWorstDeveloper.parquet")
df_Sentiment_Analysis = pd.read_parquet("df_Sentiment_Analysis.parquet")
df_ml = pd.read_parquet("df_ML.parquet")

# Endpoint de la función PlayTimeGenre: Debe devolver año con mas horas jugadas para dicho género. Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
@app.get('/PlayTimeGenre')
def PlayTimeGenre(genero : str):
    # Filtrar el DataFrame para obtener solo las filas que contienen el género específico
    filtro_genero = df_PlayTimeGenre['genres'].str.contains(genero, case=False, na=False)
    df_filtrado = df_PlayTimeGenre[filtro_genero]
    df_agrupado = df_filtrado.groupby('year')['playtime_forever'].sum().reset_index()
    # Encontrar el año con la mayor suma de 'playtime_forever'
    df_agrupado['year'] = df_agrupado['year'].astype(int)
    anio_mayor_suma = df_agrupado.loc[df_agrupado['playtime_forever'].idxmax(), 'year']
    respuesta = {f"Año de lanzamiento con más horas jugadas para Género el {genero}": anio_mayor_suma}
    return respuesta 


@app.get('/UserForGenre')
def UserForGenre(genero: str):
    # Filtrar el DataFrame para el género especificado
    filtro_genero = df_UserForGenre['genres'].str.contains(genero, case=False, na=False)
    df_filtrado = df_UserForGenre[filtro_genero]

    # Agrupar por 'user_id' y 'year', sumar las horas jugadas
    df_agrupado = df_filtrado.groupby(['user_id', 'year'])['playtime_forever'].sum().reset_index()

    # Encontrar el usuario con la máxima suma de horas jugadas
    idx_max_playtime = df_agrupado['playtime_forever'].idxmax()
    usuario_max_playtime = df_agrupado.loc[idx_max_playtime, 'user_id']

    # Filtrar el DataFrame para el usuario con máxima suma de horas jugadas
    df_usuario = df_agrupado[df_agrupado['user_id'] == usuario_max_playtime]

    # Crear el formato "Horas jugadas"
    resultado_final = [{'Año': int(row['year']), 'Horas': int(row['playtime_forever'])} for _, row in df_usuario.iterrows()]
    
    return {"Usuario con más horas jugadas para Género {}:".format(genero): usuario_max_playtime, "Horas jugadas": resultado_final}


@app.get('/UsersRecommend')
def UsersRecommend(año: int):
    
    df = df_UserRecommend[(df_UserRecommend['year_posted'] == año) & (df_UserRecommend['recommend'] == True)]

    # Contar el número de recomendaciones para cada juego
    top_juegos = df['title'].value_counts().head(3)

    # Crear el formato de salida
    resultado_final = [{"Puesto {}: {}".format(i+1, juego): recomendaciones} for i, (juego, recomendaciones) in enumerate(top_juegos.items())]

    return resultado_final


@app.get('/UsersWorstDeveloper')
def UserWorstDeveloper(year):
    # Filtrar el DataFrame por el año especificado
    df_filtered = df_UserWorstDeveloper[df_UserWorstDeveloper['year_posted'] == year]

    # Contar la cantidad de publicaciones por desarrollador
    developer_counts = df_filtered['developer'].value_counts()

    # Tomar los primeros N resultados
    top_developers = developer_counts.head(3)

    # Crear la lista con el formato solicitado
    result_list = [{"Puesto {}: {}".format(i + 1, developer): count} for i, (developer, count) in enumerate(top_developers.items())]

    return print(result_list)


@app.get('/Sentiment_Analysis')
def Sentiment_analysis(desarrollador):
    # Filtra el DataFrame para obtener la fila correspondiente al desarrollador
    desarrollador =desarrollador.lower()
    desarrollador_fila = df_Sentiment_Analysis[df_Sentiment_Analysis['Developer'] == desarrollador]

    # Extrae los valores de las columnas Negativo, Neutro y Positivo
    negativo = desarrollador_fila['Negativo'].values[0]
    neutro = desarrollador_fila['Neutro'].values[0]
    positivo = desarrollador_fila['Positivo'].values[0]

    # Crea un diccionario con la información en el formato solicitado
    resultado = {
        desarrollador: {
            'Negative': negativo,
            'Neutral': neutro,
            'Positive': positivo
        }
    }

    return resultado

@app.get('/recomendacion_usuario')
def recomendacion_usuario(user_id :str):
    # Construye una matriz de usuarios y juegos
    user_game_matrix = pd.crosstab(df_ml['user_id'], df_ml['title'])

    try:
        # Encuentra el índice del usuario en la matriz
        user_index = user_game_matrix.index.get_loc(user_id)
    except KeyError:
        print(f"El usuario {user_id} no está presente en los datos.")
        return None

    # Calcula la similitud de coseno entre los usuarios
    cosine_similarities = cosine_similarity(user_game_matrix, user_game_matrix)

    # Obtén las similitudes de coseno para el usuario dado
    similar_users = cosine_similarities[user_index]

    # Encuentra los juegos que el usuario no ha jugado
    games_played = user_game_matrix.loc[user_id]
    unrated_games = games_played[games_played == 0].index

    # Calcula las puntuaciones de recomendación sumando las similitudes de usuarios para los juegos no jugados
    recommendation_scores = user_game_matrix.loc[:, unrated_games].multiply(similar_users, axis=0).sum(axis=0)

    # Ordena las recomendaciones por puntuación descendente
    recommendations = recommendation_scores.sort_values(ascending=False).index.tolist()

    # Limita las recomendaciones a los primeros 5 juegos
    top_recommendations = recommendations[:5]

    return top_recommendations
