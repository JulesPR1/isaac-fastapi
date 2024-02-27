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
def get_items(order_by: str = None, quality: str = None, item_type: str = None, including: str = None):
    items_data = DBReader.read_items()
    if items_data is None:
        DBWriter.write_items()
        items_data = DBReader.read_items()
    
    if order_by is not None and order_by in ["id", "name", "quality"]:
      items_data = sorted(items_data, key=lambda x: int(x[order_by]) if order_by == "id" else x[order_by])
    
    if item_type is not None and item_type in ["active", "passive"]:
      active = item_type == "active"
      items_data = [item for item in items_data if item['is_active'] == active]
      
    if including is not None:
      items_data = [item for item in items_data if including in item['name'] + item['quote'] + item['description']]
       
    if quality is not None:
      items_data = [item for item in items_data if item['quality'] == quality]
      
    return items_data

@app.get("/characters")
def get_characters():
    characters_data = DBReader.read_characters()
    if characters_data is None:
        DBWriter.write_characters()
        characters_data = DBReader.read_characters()
    return characters_data
  
@app.put("/reload-db")
def reload_db():
  DBWriter.write_items()
  DBWriter.write_characters()
  return {"DB reloaded"}

@app.get("/status")
def status():
  return {"status": "OK"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}