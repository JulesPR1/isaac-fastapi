from app.utils.wiki_fetcher import WikiFetcher

class TrinketsParser:
  @staticmethod
  def parse_trinkets():
    soup = WikiFetcher.get_parsed_html("https://bindingofisaacrebirth.fandom.com/wiki/Trinkets")
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