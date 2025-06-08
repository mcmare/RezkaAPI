from dotenv import load_dotenv
import os
from HdRezkaApi import HdRezkaApi, HdRezkaSession
from HdRezkaApi.types import TVSeries, Movie
from HdRezkaApi.types import Film, Series, Cartoon, Anime
from parser import details

load_dotenv()

mirror_site = os.getenv('REZKA_MIRROR')
login_name = os.getenv('REZKA_LOGIN')
login_password = os.getenv('REZKA_PASSWORD')


#авторизация на сайте

with HdRezkaSession(mirror_site) as session:
    session.login(login_name, login_password)

if not session:
    print("Error:", str(session.exception))
    raise session.exception

def rezka(url):
    rezka = HdRezkaApi(url)
    rezka.login(login_name, login_password)
    return rezka

#Получаем поток фильма
def get_stream(id, season=1, episode=1):
    url = details(id)[0]['url']
    rez = rezka(url)
    # stream = rez.getStream(season, episode)
    stream = rez.getStream(season=1, episode=1, translation=56)
    print(stream('360p'))
    print(rez.translators)

get_stream(666)