import json
import requests
from termcolor import colored
from os import path
from threading import Thread

from app.scripts.wiki_parser import WikiParser

class DBWriter:
  
  @staticmethod
  def __get_db_path():
    return path.join(path.dirname(__file__), "json")
  
  @staticmethod
  def __get_storage_path(folder: str = None):
    return path.join(path.dirname(__file__), f"../storage/{folder}")

  @staticmethod
  def __format_item_logo_path(item):
    return f"{item['name'].lower().replace("/", " ").replace(" ", "_")}_{item['id']}_logo.png"
  
  @staticmethod
  def _write_to_file(data, file_name):
    file_path = path.join(DBWriter.__get_db_path(), file_name)
    
    with open(file_path, "w") as file:
      file.write(json.dumps(data))
    print(colored(f"{len(data)} entries written to {file_name}", "green"))

  @staticmethod
  def write_items(force: bool = False):
    items = WikiParser.parse_items()
    
    for item in items:
      DBWriter.__download_item_logo(item, force)
      item["icon"] = f"/item_images/{DBWriter.__format_item_logo_path(item)}"
      
    DBWriter._write_to_file(items, "items.json")
    

  @staticmethod
  def write_characters():
    characters = WikiParser.parse_characters()
    DBWriter._write_to_file(characters, "characters.json")

  @staticmethod
  def __download_item_logo(item, force: bool = False):
    img_name = DBWriter.__format_item_logo_path(item)
    img_path = path.join(DBWriter.__get_storage_path("items"), img_name)
    
    if not path.exists(img_path) or force:
      with open(img_path, 'wb') as f:
        f.write(requests.get(item['icon']).content)
      print(colored(f"[DOWNLOADED] {item['name']}\n------------", "green"))
    else:
      print(colored(f"[ALREADY STOCKED] {item['name']}\n------------", "yellow"))
