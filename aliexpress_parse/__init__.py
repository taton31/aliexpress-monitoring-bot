import requests
import re

from bs4 import BeautifulSoup


def re_parsing(text: str):
    result = re.search(r'\b\d(?:[ ]?\d)*\b', text)

    if result:
        number = int(result.group().replace(' ', ''))
        return number
    else:
        return -1


def get_price(url: str):
    # url = "https://aliexpress.ru/item/4001301886294.html?sku_id=12000024197341671"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.select('div[class^="snow-price_SnowPrice__main"]')
            
            return re_parsing(elements[0].text.strip())
        except Exception as e:
            print(response.text)
            print(e)
            return -1
    else:
        print("Ошибка при запросе:", response.status_code)

# print(get_price('https://aliexpress.ru/item/4001301886294.html?sku_id=12000024197341671'))
