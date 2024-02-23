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
  
print(DBReader.read_items())