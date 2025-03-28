from anilibria import Anime

from enums import API, AnimeInfo


def generate_description(anime: Anime) -> str:
    try:
        jutsu = API.jutsu.value.search(anime.name_ru)[0]
    except IndexError:
        jutsu = None
    jikan = API.jikan.value.search(search_type="anime", query=anime.name_en)["data"][0]

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
