from app.scripts.wiki_parser import WikiParser
import json
from termcolor import colored

class DBWriter:

  @staticmethod
  def write_items():
    items = WikiParser.parse_items()
    with open("db/items.json", "w") as file:
      file.write(json.dumps(items))
    print(colored(f"{len(items)} items written to db/items.json", "green"))
  
DBWriter.write_items()