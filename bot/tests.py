import json

from jikanpy import Jikan

jikan = Jikan()

# anime = jikan.random("anime")
# anime = jikan.recommendations(type="anime")
anime = jikan.top(type="anime")

# anime = jikan.search(search_type="anime", query="dandadan")
with open("data.json", "w") as file:
    json.dump(anime["data"], file, indent=4)
