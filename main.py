from typing import Optional

from fastapi import FastAPI

df_reviews = pd.read_parquet("reviews_eda.parquet")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/reviews")
def reviews(Review_number: int):
    a = df_reviews.iloc[2,5]
    return {a}
