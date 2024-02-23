from bs4 import BeautifulSoup
import requests

class WikiParser:
  @staticmethod
  def parse_items():
    unparsed_html = requests.get("https://bindingofisaacrebirth.fandom.com/wiki/Items").content
    soup = BeautifulSoup(unparsed_html, "html.parser")
    item_rows = soup.find_all("tr", class_="row-collectible")
    
    items = []
    datas = ["name", "id", "icon", "quote", "description", "quality"]
    
    for item_row in item_rows:
      item = {}
      for i, item_info in enumerate(item_row.find_all("td")):
        if i == 0:
          item[datas[i]] = item_info.find('a').text
        elif i == 1:
          for span in item_info.findAll('span'):
            span.replace_with('')
          item[datas[i]] = item_info.text.replace('\n', '')
        elif i == 2:
          item[datas[i]] = item_info.find("img")['data-src']
        elif i in [3, 4, 5]:
          item[datas[i]] = item_info.text.replace('\n', '')
        else:
          print("error " + str(i))
      items.append(item)
    
    return items