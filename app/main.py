from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from app.scripts.wiki_parser import WikiParser
from app.scripts.db_reader import DBReader
from app.scripts.db_writer import DBWriter


app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Welcome to the WikiParser API !"}

@app.get("/items")
def get_items():
    items_data = DBReader.read_items()
    if items_data is None:
        DBWriter.write_items()
        items_data = DBReader.read_items()
    return items_data

@app.get("/characters")
def get_characters():
    characters_data = DBReader.read_characters()
    if characters_data is None:
        DBWriter.write_characters()
        characters_data = DBReader.read_characters()
    return characters_data

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}