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

#Получение стрима
def get_stream(id, season=1, episode=1):
    stream_box = []
    url = details(id)[0]['url']
    with HdRezkaSession(mirror_site) as session:
        session.login(login_name, login_password)
        rezka = session.get(url)


    # rezka = HdRezkaApi(url)
    if not rezka.ok:
        print("Error:", str(rezka.exception))
        raise rezka.exception

    stream = rezka.getStream(season, episode)
    if stream('360p'):
       res_360p = stream('360p')[0]
       stream_box.append({'360p': res_360p})
    if stream('480p'):
        res_480p = stream('480p')[0]
        stream_box.append({'480p': res_480p})
    if stream('720p'):
        res_720p = stream('720p')[0]
        stream_box.append({'720p': res_720p})
    if stream('1080p'):
        res_1080p = stream('1080p')[0]
        stream_box.append({'1080p': res_1080p})
    return stream_box
