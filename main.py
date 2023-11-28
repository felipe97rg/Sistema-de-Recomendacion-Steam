from typing import Optional

from fastapi import FastAPI

import pandas as pd

df_reviews = pd.read_parquet("reviews_eda.parquet")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/reviews")
def reviews(Review_number: int):
    a = df_reviews.iloc[Review_number,5]
    return {a}
