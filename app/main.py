from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from scripts.wiki_parser import WikiParser
from scripts.db_reader import DBReader
from scripts.db_writer import DBWriter


app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Welcome to the WikiParser API": "Use /items to get the list of items"}

@app.get("/items")
def get_items():
    if DBReader.read_items() == None:
      DBWriter.write_items()
    return DBReader.read_items()

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}