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


#Получаем катеогории и ссылки на них
def get_main_category():
    # Получаем теги a с категориями
    categories = []

    re = soup.find_all('a', class_='b-topnav__item-link')
    # Перечисляем категории и ссылки на них
    for data in re:
        index = re.index(data)
        category_id = index
        category_name = re[index].text.strip()
        category_url = re[index].get('href')
        categories.append({'id':category_id, 'name':category_name, 'url':category_url})
    return categories

# req = get_main_category()
# print(req)