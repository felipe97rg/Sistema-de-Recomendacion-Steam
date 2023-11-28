from typing import Optional

from fastapi import FastAPI

import pandas as pd

df_reviews = pd.read_parquet("reviews_eda.parquet")
df_PlayTimeGenre = pd.read_parquet("df_PlayTimeGenre.parquet")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/reviews")
def reviews(Review_number: int):
    a = df_reviews.iloc[Review_number,5]
    return {a}

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
