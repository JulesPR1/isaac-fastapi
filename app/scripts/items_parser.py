from app.utils.wiki_fetcher import WikiFetcher

class ItemsParser:  
  @staticmethod
  def parse_items():
    soup = WikiFetcher.get_parsed_html("https://bindingofisaacrebirth.fandom.com/wiki/Items")
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
  
  # TODO finish this
  @staticmethod
  def parse_item_details(item_name):
    formatted_name = ItemsParser.__format_name(item_name)
    
    soup = WikiFetcher.get_parsed_html(f"https://bindingofisaacrebirth.fandom.com/wiki/{formatted_name}")
    content = soup.find('div', id="content")

    data = {}
    
    data["item_pool"] = content.find("span", class_="item-pool-list-pool").find_all("a")[-1].text
    
    return data
  

  @staticmethod
  def __format_name(name):
    name = name.split(" ")
    item_name_formatted = []
    
    for word in name:
      word.capitalize()
      item_name_formatted.append(word.capitalize())
    
    item_name_formatted = "_".join(item_name_formatted)
    
    return item_name_formatted