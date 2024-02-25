from app.scripts.wiki_parser import WikiParser
import json
from termcolor import colored
from os import path

class DBWriter:
  
  @staticmethod
  def __get_db_path():
    return path.join(path.dirname(__file__), "../db")
  
  @staticmethod
  def _write_to_file(data, file_name):
    file_path = path.join(DBWriter.__get_db_path(), file_name)
    with open(file_path, "w") as file:
      file.write(json.dumps(data))
    print(colored(f"{len(data)} entries written to {file_name}", "green"))

  @staticmethod
  def write_items():
    items = WikiParser.parse_items()
    DBWriter._write_to_file(items, "items.json")

  @staticmethod
  def write_characters():
    characters = WikiParser.parse_characters()
    DBWriter._write_to_file(characters, "characters.json")
