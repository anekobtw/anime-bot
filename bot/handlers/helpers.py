from anilibria import Anime

from enums import API, AnimeInfo


def generate_description(anime: Anime) -> str:
    jikan = API.jikan.value.search(search_type="anime", query=anime.name_en)["data"][0]

    return "".join(AnimeInfo.DESCRIPTION.value).format(
        name_ru=anime.name_ru,
        year=f"{anime.season.capitalize()} {anime.year}",
        rating=jikan["score"],
        in_favorites=anime.in_favorites,
        genres=", ".join(anime.genres),
        status=anime.status,
        episodes=anime.episodes_count,
        episodes_length=anime.episode_length,
        description=f"{".".join(anime.description.split(".")[:3])}...",
        trailer=jikan["trailer"]["url"],
        link_jutsu=f"https://jut.su/" + anime.code,
        link_anilibria="https://www.anilibria.top/anime/releases/release/" + anime.code + "/episodes",
    )
