from bs4 import BeautifulSoup
import requests

class WikiFetcher:
  
  @staticmethod
  def get_parsed_html(url):
    url = url
    headers = {
      "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    raw_html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(raw_html, "html.parser")
    
    return soup