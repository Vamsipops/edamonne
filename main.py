from fastapi import FastAPI
from horoscope import horoscope_routes

app = FastAPI()

app.include_router(horoscope_routes)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

