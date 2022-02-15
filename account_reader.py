import requests
from bs4 import BeautifulSoup

def return_money(contents: ['']) -> int:
    collected_money = ''
    for content in contents:
        number = content
        try:
            number = int(str(content))
            collected_money += content
        except ValueError as e:
            continue
    
    return int(collected_money) if collected_money != '' else None

def scrap_from_web(url: str) -> (int, int):
    web_doc = requests.get(url)
    doc = BeautifulSoup(web_doc.text, "html.parser")
    price = doc.find_all(text="₽")
    collected_contents = price[0].parent.parent.contents
    needed_contents = price[1].parent.parent.contents
    return (return_money(collected_contents), return_money(needed_contents))
