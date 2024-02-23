from os import path
import json

class DBReader:
  @staticmethod
  def read_items():
    file_path = "db/items.json"
    if not path.exists(file_path):
      return None
    with open(file_path, "r") as file:
      items = file.read()
    return json.loads(items)
  
print(DBReader.read_items())