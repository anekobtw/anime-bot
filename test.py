import time

import crunpyroll
import requests
from AnilistPython import Anilist
from jikanpy import Jikan

s = time.time()

# anime = get_anilist_id("Kuroko no Basket")

# crunpyroll = crunpyroll.Client()
# anime = crunpyroll.search("Kuroko no Basket")

jikan = Jikan()
anime = jikan.search(search_type="anime", query="solo leveling")["data"][0]


e = time.time()
print(anime)
print(e - s)
