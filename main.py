from typing import Optional

from fastapi import FastAPI

import pandas as pd


app = FastAPI()

df_Sentiment_Analysis = pd.read_parquet("df_Sentiment_Analysis.parquet")

@app.get('/Sentiment_Analysis')
def Sentiment_Analysis(desarrollador):
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
