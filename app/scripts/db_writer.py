from app.scripts.wiki_parser import WikiParser
import json
from termcolor import colored
from os import path

class DBWriter:
  
  @staticmethod
  def write_items():
    items = WikiParser.parse_items()
    
    db_path = path.join(path.dirname(__file__), "../db/items.json")
    
    with open(db_path, "w") as file:
      file.write(json.dumps(items))
      
    print(colored(f"{len(items)} items written to db/items.json", "green"))
