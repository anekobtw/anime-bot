from datetime import datetime

import pymorphy3
import requests
from anilibria.models import Anime
from dateutil.relativedelta import relativedelta

from enums import API, AnimeInfo

morph = pymorphy3.MorphAnalyzer()


def generate_links(anime_id: int) -> str:
    def get_anilist_id(title: str) -> int | None:
        q = "query($search:String){Media(search:$search,type:ANIME){id}}"
        r = requests.post("https://graphql.anilist.co", json={"query": q, "variables": {"search": title}})
        return r.json().get("data", {}).get("Media", {}).get("id")

    anilibria = API.anilibria.value.search_id(anime_id)
    jikan = API.jikan.value.search(anilibria.name_en)["data"][0]
    anilist_url = f"https://anilist.co/anime/{get_anilist_id(anilibria.name_en)}"
    jutsu = API.jutsu.value.search(anilibria.name_ru)[0]

    return AnimeInfo.LINKS.value.format(
        trailer=jikan["trailer"]["url"],
        anilist=anilist_url,
        jikan=jikan["url"],
        anilibria=f"https://www.anilibria.top/anime/releases/release/{anilibria.code}/episodes",
        jutsu=f"https://jut.su/{jutsu.id}",
    )


def generate_description(anime: Anime) -> str:
    description = AnimeInfo.DESCRIPTION.value.format(
        name=anime.name_ru,
        year=f"{anime.season.capitalize()} {anime.year}",
        in_favorites=anime.in_favorites,
        genres=", ".join(anime.genres),
        status=anime.status,
        type=anime.type,
        description=f"{'.'.join(anime.description.split('.')[:3])}...",
    )

    return description


def pluralize(word: str, number: int) -> str:
    parsed = morph.parse(word)[0]
    if number % 10 == 1 and number % 100 != 11:
        return parsed.inflect({"nomn"}).word  # Именительный
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return parsed.inflect({"gent"}).word  # Родительный ед. числа
    else:
        return parsed.inflect({"gent"}).inflect({"plur"}).word  # Родительный мн. числа


def get_relative_time(timestamp: int) -> str:
    updated_time = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = relativedelta(now, updated_time)

    if diff.years > 0:
        return f"{diff.years} {pluralize('год', diff.years)} назад"
    elif diff.months > 0:
        return f"{diff.months} {pluralize('месяц', diff.months)} назад"
    elif diff.days > 0:
        return f"{diff.days} {pluralize('день', diff.days)} назад"
    elif diff.hours > 0:
        return f"{diff.hours} {pluralize('час', diff.hours)} назад"
    elif diff.minutes > 0:
        return f"{diff.minutes} {pluralize('минута', diff.minutes)} назад"
    else:
        return "только что"
