from typing import Union

from fastapi import FastAPI

from settings import get_settings

settings = get_settings()
app = FastAPI()


@app.get("/health")
def read_root():
    return {"status": "healthy"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
