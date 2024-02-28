import json
import requests
from termcolor import colored
from os import path

from app.scripts.wiki_parser import WikiParser

class DBWriter:
  
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
      img_name = DBWriter.__download_img(img_storage_path="items", img=item["img"], img_name=item["name"].replace(" ", "_").replace("/", "_").lower(), force=force)
      item["img"] = f"item_images/{img_name}"
      
    DBWriter._write_to_file(items, "items.json")
    
  @staticmethod
  def write_trinkets(force: bool = False):
    trinkets = WikiParser.parse_trinkets()
    
    for trinket in trinkets:
      img_name = DBWriter.__download_img(img_storage_path="trinkets", img=trinket["img"], img_name=trinket["name"].replace(" ", "_").replace("/", "_").lower(), force=force)
      trinket["img"] = f"trinket_images/{img_name}"
      
    DBWriter._write_to_file(trinkets, "trinkets.json")
    
    
  @staticmethod
  def write_characters(force: bool = False):
    characters = WikiParser.parse_characters()
    
    for character in characters:
      img_name = DBWriter.__download_img(img_storage_path="characters", img=character["img"], img_name=character["name"].replace(" ", "_").lower(), force=force)
      character["img"] = f"character_images/{img_name}"
      
    DBWriter._write_to_file(characters, "characters.json")
    
  
  @staticmethod
  def __get_db_path():
    return path.join(path.dirname(__file__), "json")
  
  
  @staticmethod
  def __get_storage_path(folder: str = None):
    return path.join(path.dirname(__file__), f"../storage/{folder}")
  

  @staticmethod
  def __format_img_path(img_name: str):
    return f"{img_name.lower().replace('/', ' ').replace(' ', '_')}.png"
  
  
  @staticmethod
  def __download_img(img_storage_path, img, img_name, force: bool = False):
    img_name = DBWriter.__format_img_path(img_name)
    img_path = path.join(DBWriter.__get_storage_path(img_storage_path), img_name)
    
    if not path.exists(img_path) or force:
      with open(img_path, 'wb') as f:
        f.write(requests.get(img).content)
      print(colored(f"[IMAGE DOWNLOADED] {img_name}\n------------------", "green"))
    else:
      print(colored(f"[IMAGE ALREADY EXISTS] {img_name}\n------------------", "yellow"))
    
    return img_name