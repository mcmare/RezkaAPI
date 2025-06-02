from HdRezkaApi import HdRezkaApi, HdRezkaSession
from HdRezkaApi.types import TVSeries, Movie
from HdRezkaApi.types import Film, Series, Cartoon, Anime

# url = "https://rezka.fi/series/comedy/1154-teoriya-bolshogo-vzryva-2007-latest.html"

with HdRezkaSession("https://rezka.fi/") as session:
	session.login("admin@mcmare.ru", "8700192Www")
	rezka = session.get("https://rezka.fi/films/fiction/666-kovboi-protiv-prishelcev-2012.html")


# rezka = HdRezkaApi(url)
if not rezka.ok:
	print("Error:", str(rezka.exception))
	raise rezka.exception

stream = rezka.getStream(1, 5)
print(stream('720p'))