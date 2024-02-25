from os import path, pardir
import json

class DBReader:
  @staticmethod
  def read_items():
    
    db_path = path.join(path.dirname(__file__), "../db/items.json")
    
    if not path.exists(db_path):
      print("No items found in db/items.json")
      return None
    with open(db_path, "r") as file:
      items = file.read()
    return json.loads(items)
  
  def read_characters():
    db_path = path.join(path.dirname(__file__), "../db/characters.json")
    
    if not path.exists(db_path):
      print("No characters found in db/characters.json")
      return None
    with open(db_path, "r") as file:
      characters = file.read()
    return json.loads(characters)