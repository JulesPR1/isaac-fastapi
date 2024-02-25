from os import path, pardir
import json

class DBReader:
  @staticmethod
  def _read_json(file_path):
    if not path.exists(file_path):
      print(f"No data found in {file_path}")
      return None
    with open(file_path, "r") as file:
      data = file.read()
    return json.loads(data)

  @staticmethod
  def read_items():
    db_path = path.join(path.dirname(__file__), "../db/items.json")
    return DBReader._read_json(db_path)

  @staticmethod
  def read_characters():
    db_path = path.join(path.dirname(__file__), "../db/characters.json")
    return DBReader._read_json(db_path)