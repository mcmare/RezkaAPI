from operator import index

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

url_login = "https://rezka.fi/ajax/login/"
url_site = "https://rezka.fi"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
data_login = {
    'login_name': os.getenv('REZKA_LOGIN'),
    'login_password': os.getenv('REZKA_PASSWORD')
}
session = requests.Session()
session.headers.update(headers)
# Получаем Сессию
response = session.post(url_login, data=data_login)

if response.json()['success']:
    print("Вы успешно авторизованы")
if not response.json()['success']:
    print(response.json()['message'])

# Получаем сайт после авторизации
page = session.post(url_site)
# Парсим в суп
soup = BeautifulSoup(page.text, "html.parser")


def get_topnav_item():
    list_id = []
    re = soup.find_all('li', attrs={'class': lambda value: value and "b-topnav__item" in value})
    for item in re:
        index = (re.index(item))
        list_id.append(f"{item.get('class')[0]} {item.get('class')[1]} ")
    return list_id

# print(get_topnav_item())

#Получаем катеогории и ссылки на них
def get_main_category():
    # Получаем теги a с категориями
    categories = []

    re = soup.find_all('a', class_='b-topnav__item-link')
    # Перечисляем категории и ссылки на них
    for data in re:
        category_id = re.index(data)
        category_name = re[category_id].text.strip()
        category_url = re[category_id].get('href')
        li_id = get_topnav_item()[category_id]
        categories.append({'id':category_id, 'name':category_name, 'url':category_url, 'li_id':li_id})
    return categories

# print(get_main_category())

def get_main_subcategory(category_id):
    # subcategories = []
    # re = soup.find_all('li', attrs={'class': lambda value: value and "b-topnav__item" in value})
    # for data in re:
    #     req = data.find_all('ul', class_='left')
    #     # print(req)
    #     subcategory_id = re.index(data)
    #     for n in range(category_id):
    #         req = n.find('li')
    #         print(req)
    #         subcategory_name = re[subcategory_id].text.strip()
    #     # subcategories.append()
    # return subcategories

get_main_subcategory(0)

def list_category(list_id):
    pass