from typing import Optional

from fastapi import FastAPI

import pandas as pd


app = FastAPI()

df_Sentiment_Analysis = pd.read_csv("df_Sentiment_Analysis.csv")

@app.get('/Sentiment_Analysis')
def sentiment_analysis(empresa_desarrolladora : str):
    
    # Filtrar el DataFrame por la empresa desarrolladora especificada
    df_empresa = df_Sentiment_Analysis[df_Sentiment_Analysis['developer'] == empresa_desarrolladora]

    # Contar la cantidad de registros por análisis de sentimiento
    conteo_sentimientos = df_empresa['sentiment_analysis'].value_counts()

    # Crear el diccionario de resultados en el formato deseado
    resultado = {empresa_desarrolladora: {'Negative': conteo_sentimientos.get(0, 0),
                                           'Neutral': conteo_sentimientos.get(1, 0),
                                           'Positive': conteo_sentimientos.get(2, 0)}}

    return resultado
