import asyncio
from typing import Any

from anilibria import Anime

from enums import API, AnimeInfo


async def fetch_anime_data(anime: Anime) -> tuple[Any | None, Any]:
    async def get_jutsu() -> Any | None:
        try:
            return (await asyncio.to_thread(API.jutsu.value.search, anime.name_ru))[0]
        except IndexError:
            return None

    async def get_jikan() -> Any:
        try:
            result = await asyncio.to_thread(API.jikan.value.search, search_type="anime", query=anime.name_en)
            return result["data"][0]
        except IndexError:
            return None

    jutsu, jikan = await asyncio.gather(get_jutsu(), get_jikan())

    return jutsu, jikan



async def generate_description(anime: Anime) -> str:
    jutsu, jikan = await fetch_anime_data(anime)

    return "".join(AnimeInfo.DESCRIPTION.value).format(
        name=anime.name_ru,
        year=f"{anime.season.capitalize()} {anime.year}",
        age=f", {jutsu.age}+" if jutsu else "",
        rating=jikan["score"],
        in_favorites=anime.in_favorites,
        genres=", ".join(anime.genres),
        status=anime.status,
        type=anime.type,
        description=f"{".".join(anime.description.split(".")[:3])}...",
        trailer=jikan["trailer"]["url"],
        link_jutsu=f"https://jut.su/{jutsu.name.id}" if jutsu else None,
        link_anilibria="https://www.anilibria.top/anime/releases/release/" + anime.code + "/episodes",
    )
