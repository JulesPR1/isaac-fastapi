from typing import Union

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

import time
import datetime

from os import path

from app.db.db_reader import DBReader
from app.db.db_writer import DBWriter

router = APIRouter()
app = FastAPI()

app.mount("/item_images", StaticFiles(directory=path.join(path.dirname(__file__), f"storage/items")), name="item_images")
app.mount("/trinket_images", StaticFiles(directory=path.join(path.dirname(__file__), f"storage/trinkets")), name="trinket_images")
app.mount("/character_images", StaticFiles(directory=path.join(path.dirname(__file__), f"storage/characters")), name="character_images")

@app.get("/")
def read_root():
  return {"Welcome to the Isaac API !"}


@app.get("/items")
def get_items(order_by: str = None, quality: str = None, item_type: str = None, including: str = None):
  """
  Retrieve a list of items based on the specified filters.

  Parameters:
  - order_by (str): The field to order the items by. Valid values are "id", "name", and "quality".
  - quality (str): The quality of the items to retrieve.
  - item_type (str): The type of items to retrieve. Valid values are "active" and "passive".
  - including (str): A string that the item's name, quote, or description should include.

  Returns:
  - List[Dict[str, Any]]: A list of items that match the specified filters.
  """
  items_data = DBReader.read("items")
  if items_data is None:
    DBWriter.write_items()
    items_data = DBReader.read("items")

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

@app.get("/trinkets")
def get_items(order_by: str = None, including: str = None):
  """
  Retrieve trinkets based on specified filters.

  Parameters:
  - order_by (str): Optional. Specifies the field to order the trinkets by. Can be 'id', 'name', or 'quality'.
  - including (str): Optional. Specifies a keyword to filter trinkets by, including the name, quote, and description.

  Returns:
  - List[Dict]: A list of trinkets that match the specified filters.
  """
  trinkets_data = DBReader.read("trinkets")
  if trinkets_data is None:
    DBWriter.write_trinkets()
    trinkets_data = DBReader.read("trinkets")

  if order_by is not None and order_by in ["id", "name", "quality"]:
    trinkets_data = sorted(trinkets_data, key=lambda x: int(x[order_by]) if order_by == "id" else x[order_by])

  if including is not None:
    trinkets_data = [trinket for trinket in trinkets_data if including in trinket['name'] + trinket['quote'] + trinket['description']]

  return trinkets_data


@app.get("/characters")
def get_characters():
  """
  Retrieve the characters data from the database.

  If the characters data is not found in the database, it will be written to the database
  using the DBWriter.write_characters() method before retrieving it again.

  Returns:
  - List[Dict[str, Any]] The characters data from the database.
  """
  characters_data = DBReader.read("characters")

  if characters_data is None:
    DBWriter.write_characters()
    characters_data = DBReader.read("characters")

  return characters_data

  
@app.put("/reload-db")
def reload_db(reload_images: bool = False):
  """
  Reloads the database by writing items and characters to the database.
  
  Args:
    reload_images (bool, optional): Whether to reload images or not. Defaults to False. Reloading images can take a long time.
  
  Returns:
    dict: A dictionary containing the elapsed time in seconds for the database reload.
  """
  start = time.time()
  
  DBWriter.write_items(force=reload_images)
  DBWriter.write_trinkets(force=reload_images)
  DBWriter.write_characters(force=reload_images)
  
  end = time.time()
  
  elapsed_time_seconds = end - start
  elapsed_time_readable = "{:.1f}".format(elapsed_time_seconds)
  
  return {"DB reloaded in": f"{elapsed_time_readable}s"}


@app.get("/status")
def status():
  """
  Returns the status of the application.

  :return: A dictionary containing the status message.
  :rtype: dict
  """
  return {"status": "OK"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}