from typing import Optional

from fastapi import FastAPI

import pandas as pd

df_reviews = pd.read_parquet("reviews_eda.parquet")
df_items = pd.read_parquet("items_eda.parquet")
df_games = pd.read_parquet("games_eda.parquet")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/reviews")
def reviews(Review_number: int):
    a = df_reviews.iloc[Review_number,5]
    return {a}

@app.get('/PlayTimeGenre')
def PlayTimeGenre(genero : str):
     # Reemplazar los valores nulos en la columna 'genres' con una cadena vacía
    df_games['genres'].fillna('', inplace=True)

    # Filtrar el DataFrame para obtener solo las filas que contienen el género específico
    filtro_genero = df_games['genres'].str.contains(genero, case=False, na=False)
    df_filtrado = df_games[filtro_genero]

    # Agrupar por 'item_id' y sumar los valores de 'playtime_forever'
    playtiem_item = df_items.groupby('item_id')['playtime_forever'].sum().reset_index()

    df_merge = pd.merge(df_filtrado, playtiem_item, on='item_id', how='inner')

    df_agrupado = df_merge.groupby('year')['playtime_forever'].sum().reset_index()


    # Encontrar el año con la mayor suma de 'playtime_forever'
    df_agrupado['year'] = df_agrupado['year'].astype(int)
    anio_mayor_suma = df_agrupado.loc[df_agrupado['playtime_forever'].idxmax(), 'year']
    respuesta = {f"Año de lanzamiento con más horas jugadas para Género {genero}": anio_mayor_suma}
    return respuesta
