from bs4 import BeautifulSoup
import requests

class WikiParser:
  
  @staticmethod
  def parse_items():
    soup = WikiParser.__get_parsed_html("https://bindingofisaacrebirth.fandom.com/wiki/Items")
    item_rows = soup.find_all("tr", class_="row-collectible")
    
    items = []
    datas = ["name", "id", "img", "quote", "description", "quality"]
    
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
          if len(item_info.find_all("div")) > 0: # if the item is active (because only active items have a div in the img column)
            item[datas[i]] = item_info.find("img")['data-src']
            item["is_active"] = True
          else:
            item[datas[i]] = item_info.find("img")['data-src']
            item["is_active"] = False
        elif i in [3, 4, 5]:
          item[datas[i]] = item_info.text.replace('\n', '')
        else:
          print("error " + str(i))
      items.append(item)
    return items
  
  @staticmethod
  def parse_trinkets():
    soup = WikiParser.__get_parsed_html("https://bindingofisaacrebirth.fandom.com/wiki/Trinkets")
    trinket_rows = soup.find_all("tr", class_="row-trinket")
    
    trinkets = []
    datas = ["name", "id", "img", "quote", "description"]
    
    for trinket_row in trinket_rows:
      trinket = {}
      for i, trinket_info in enumerate(trinket_row.find_all("td")):
        if i == 0:
          trinket[datas[i]] = trinket_info.find('a').text
        elif i == 1:
          for span in trinket_info.findAll('span'):
            span.replace_with('')
          trinket[datas[i]] = trinket_info.text.replace('\n', '')
        elif i == 2:
          trinket[datas[i]] = trinket_info.find("img")['data-src']
          trinket["is_active"] = True
        elif i in [3, 4]:
          trinket[datas[i]] = trinket_info.text.replace('\n', '')
        else:
          print("error " + str(i))
      trinkets.append(trinket)
    return trinkets
  
  # TODO finish this
  @staticmethod
  def parse_item_details(item_name):
    formatted_name = WikiParser.__format_name(item_name)
    
    soup = WikiParser.__get_parsed_html(f"https://bindingofisaacrebirth.fandom.com/wiki/{formatted_name}")
    content = soup.find('div', id="content")

    data = {}
    
    data["item_pool"] = content.find("span", class_="item-pool-list-pool").find_all("a")[-1].text
    
    return data
  
  
  @staticmethod
  def parse_characters():
    soup = WikiParser.__get_parsed_html(f"https://bindingofisaacrebirth.fandom.com/wiki/Characters#Tainted_Characters")
    table_body = soup.find_all("table", class_="wikitable")[0].find("tbody")    

    
    characters = WikiParser.__init_characters(table_body, subcharacter=False)
    sub_characters = WikiParser.__init_characters(table_body, subcharacter=True)[::-1] # reversing subcharacters for assignement
    
    data = characters

    for i, character in enumerate(characters):
      if i in [3, 8, 14, 16]:
        character["sub_characters"] = [sub_characters.pop(), sub_characters.pop()]
            
    for i, tr in enumerate(table_body.find_all("tr")[2:12]):
      if not tr.find("th"):
        continue
      
      header = tr.find("th").text
      if not header:
        header = tr.find("th").find("a").text

      header = header.strip().lower()
      tr_tds = tr.find_all("td")
         
      if len(tr_tds) == 0:
        continue
      
      characters = WikiParser.__reorder_characters_woth_subcharacters(characters)
      
      # skip one column for the 7 and 8th row after the 17th column (due to the subcharacters)
      for k, character in enumerate(characters):
        if k >= 17 and i in [7,8]: 
          td = tr_tds[k-1]
        else: 
          td = tr_tds[k] 
        
        if i == 1:
          character[header] = WikiParser.__get_life_dict(td.find_all("img"))
        else:
          character[header] = td.text.strip().replace("\n", "")

    for character in data:
      character["achievements"] = []
    
    # achievement
    for i, tr in enumerate(table_body.find_all("tr")[13:]):
      if not tr.find("th"):
        continue
      
      header = tr.find("th").text
      if not header:
        header = tr.find("th").find("a").text

      header = header.strip().lower()
      tr_tds = tr.find_all("td")
         
      if len(tr_tds) == 0:
        continue
      
      for k, character in enumerate(data):
        td = tr_tds[k]
        character["achievements"].append({"condition": header, "unlockable": td.find("img")["alt"]}) 

    return data
  

  # private methods
  @staticmethod
  def __format_name(name):
    name = name.split(" ")
    item_name_formatted = []
    
    for word in name:
      word.capitalize()
      item_name_formatted.append(word.capitalize())
    
    item_name_formatted = "_".join(item_name_formatted)
    
    return item_name_formatted
  
  
  @staticmethod
  def __get_parsed_html(url):
    url = url
    headers = {
      "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    raw_html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(raw_html, "html.parser")
    
    return soup
  
  
  @staticmethod
  def __get_life_dict(imgs):
    data = []
    for img in imgs:
      if "heart" in img['alt']:
        data.append(img['alt'])
      elif "Random" in  img['alt']:
        return ["Random"]
      
    return data
  
  
  @staticmethod
  def __init_characters(table_body, subcharacter: bool):
    data = []
    for th in table_body.find_all("tr")[2 if subcharacter else 1].find_all("th"):
      character = {}
      name = th.find_all("a")[-1].text    
      character["name"] = name
      for span in th.findAll('span'):
        span.replace_with('')
      if th.find("img"):
        if th.find("img").has_attr("data-src"):
          character["img"] = th.find("img")["data-src"]
        else:
          character["img"] = th.find("img")["src"]
      data.append(character)
    return data
  

  @staticmethod
  def __reorder_characters_woth_subcharacters(characters):
    data = []
    
    for character in characters:
      if "sub_characters" not in character:
        data.append(character)
      else:
        for sub_character in character["sub_characters"]:
          data.append(sub_character)

    return data
