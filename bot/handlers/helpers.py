from datetime import datetime
from typing import Any

import pymorphy3
from anilibria.models import Anime
from dateutil.relativedelta import relativedelta

from enums import API, AnimeInfo, Keyboards

morph = pymorphy3.MorphAnalyzer()


def fetch_link(fetch_func) -> Any | None:
    try:
        return fetch_func()
    except Exception:
        return None


def generate_links(anime_id: int) -> str:
    anilibria = API.anilibria.value.search_id(anime_id)
    jikan = fetch_link(lambda: API.jikan.value.search(search_type="anime", query=anilibria.name_en)).get("data", None)[0]
    jutsu = fetch_link(lambda: API.jutsu.value.search(anilibria.name_ru))

    return Keyboards.links(
        trailer=jikan["trailer"]["url"] if jikan else None,
        anilibria=f"https://www.anilibria.top/anime/releases/release/{anilibria.code}/episodes",
        jutsu=f"https://jut.su/{jutsu[0].name.id}" if jutsu else None,
    )


def generate_description(anime: Anime) -> str:
    return AnimeInfo.DESCRIPTION.value.format(
        name=anime.name_ru,
        year=f"{anime.season.capitalize()} {anime.year}",
        in_favorites=anime.in_favorites,
        genres=", ".join(anime.genres),
        type=anime.type,
        description=f"{'.'.join(anime.description.split('.')[:3])}...",
    )


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
