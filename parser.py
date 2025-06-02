import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from sqlalchemy.orm.unitofwork import track_cascade_events
from unicodedata import category

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


# Получаем класс тега li на верхнее меню
def get_topnav_item():
    list_id = []
    re = soup.find_all('li', attrs={'class': lambda value: value and "b-topnav__item" in value})
    for item in re:
        index = (re.index(item))
        list_id.append(f"{item.get('class')[0]} {item.get('class')[1]} ")
    return list_id


# print(get_topnav_item())

# Получаем категории и ссылки на них
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
        categories.append({'id': category_id, 'name': category_name, 'url': category_url, 'li_id': li_id})
    return categories


# Получаем подкатегории из категорий меню
def get_main_subcategory(category_id):
    subcategories = []
    if category_id <= 3:
        re = soup.find_all('li', attrs={'class': lambda value: value and 'b-topnav__item ' in value})[category_id]
        re = re.find_all('ul', class_='left')[0]
        re = re.find_all('li')
        for data in re:
            req = data.find_all('a')
            subcategory_id = re.index(data)
            subcategory_name = re[subcategory_id].text.strip()
            subcategory_url = req[0].get('href')
            subcategories.append({'id': subcategory_id, 'name': subcategory_name, 'url': subcategory_url})
    else:
        re = soup.find_all('li', attrs={'class': lambda value: value and 'b-topnav__item ' in value})[category_id]
        req = re.find('a')
        subcategory_id = 0
        subcategory_name = re.text.strip()
        subcategory_url = req.get('href')
        subcategories.append({'id': subcategory_id, 'name': subcategory_name, 'url': subcategory_url})
    return subcategories


#Получаем список фильмов в категории
def get_list_in_category(category_id, pages=1):
    list_in_category = []
    category = get_main_category()
    if pages == 1:
        page = session.post(url_site + category[category_id]['url'])
    else:
        page = session.post(url_site + category[category_id]['url'] + 'page/' + str(pages))
    soup = BeautifulSoup(page.text, "html.parser")
    re = soup.find_all('div', class_='b-content__inline_item')
    for data in re:
        # print(data)
        id = data.get('data-id')
        img = data.select('div.b-content__inline_item-cover img')[0].get('src')
        # print(img)
        href = data.select('div.b-content__inline_item-link a')[0].get('href')
        text = data.select('div.b-content__inline_item-link a')[0].text
        list_in_category.append({'id': id, 'img': img, 'href': href, 'text': text})
    return list_in_category

#Получаем список коллекций
def get_collections(pages=1):
    list_collections = []
    page = session.post(url_site + "/collections/" + "page/" + str(pages) + "/")
    soup = BeautifulSoup(page.text, "html.parser")
    re = soup.find_all('div', class_ = 'b-content__collections_item')
    for data in re:
        id = re.index(data)
        num = data.find('div', class_ = 'num').text
        img = data.find('img', class_ = 'cover').get('src')
        href = data.find('a', class_ = 'title').get('href')
        text = data.find('a', class_ = 'title').text
        list_collections.append({'id': id, 'num': num, 'img': img, 'href': href, 'text': text})
    return list_collections

#Получаем список в фильмов в поиске
def search_content(query, pages=1):
    search_list = []
    search_url = f"{url_site}/search/?do=search&subaction=search&q={query}&page={pages}"
    page = session.post(search_url)
    soup = BeautifulSoup(page.text, "html.parser")
    re = soup.find_all('div', class_ = 'b-content__inline_item')
    for data in re:
        id = int(data.attrs["data-id"])
        type = data.find('i', class_='entity').text
        title = data.find('div', class_='b-content__inline_item-link').find('a').text
        url = data.find('div').find('a').get('href')
        img = data.find('img').get('src')
        search_list.append({'id': id, 'img': img, 'type': type, 'title': title, 'url': url})
    return search_list

def details(id):
    details = []
    details_url = f"{url_site}/engine/ajax/quick_content.php?id={id}&is_touch=1"
    page = session.get(details_url)
    soup = BeautifulSoup(page.text, "html.parser")
    url = soup.find('div', class_='b-content__bubble_title').find('a').get('href')
    type = soup.find('i', class_='entity').text
    title = soup.find('div', class_='b-content__bubble_title').find('a').text
    description = soup.find('div', class_='b-content__bubble_text').text
    page = session.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    img = soup.find('div', class_='b-post__infotable_left').find('img').get('src')
    print(img)
    details.append({'id': id, 'url': url, 'type': type, 'title': title, 'description': description, 'img': img})
    return details

def get_translate(id):
    translates = []
    url = f"{url_site}/engine/ajax/quick_content.php?id={id}&is_touch=1"
    page = session.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    url = soup.find('div', class_='b-content__bubble_title').find('a').get('href')
    page = session.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    tr = soup.find('div', class_='b-translators__block').find_all('li')
    for i in tr:
        tr_id = i.get('data-translator_id')
        tr_director = i.get('data-director')
        tr_title = i.get('title')
        translates.append({'id': tr_id, 'director': tr_director, 'title': tr_title})
    return translates

