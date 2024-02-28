from app.utils.wiki_fetcher import WikiFetcher

class CharactersParser:
  
  @staticmethod
  def parse_characters():
    soup = WikiFetcher.get_parsed_html(f"https://bindingofisaacrebirth.fandom.com/wiki/Characters#Tainted_Characters")
    table_body = soup.find_all("table", class_="wikitable")[0].find("tbody")    

    
    characters = CharactersParser.__init_characters(table_body, subcharacter=False)
    sub_characters = CharactersParser.__init_characters(table_body, subcharacter=True)[::-1] # reversing subcharacters for assignement
    
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
      
      characters = CharactersParser.__reorder_characters_woth_subcharacters(characters)
      
      # skip one column for the 7 and 8th row after the 17th column (due to the subcharacters)
      for k, character in enumerate(characters):
        if k >= 17 and i in [7,8]: 
          td = tr_tds[k-1]
        else: 
          td = tr_tds[k] 
        
        if i == 1:
          character[header] = CharactersParser.__get_life_dict(td.find_all("img"))
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
