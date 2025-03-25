from enums import API, AnimeInfo


def generate_description(anime_id: str) -> list[str, str]:
    anime_jutsu = API.jutsu.value.anime(anime_id)
    anime_jikan = API.jikan.value.search(search_type="anime", query=anime_jutsu.name.orig)["data"][0]

    return (
        anime_jikan["images"]["jpg"]["large_image_url"],
        "".join(AnimeInfo.DESCRIPTION.value).format(
            emoji="🔞" if anime_jutsu.age >= 18 else "🍿",
            name=anime_jutsu.name.name,
            types=", ".join([t.name for t in anime_jutsu.info.types]),
            years=", ".join(map(str, anime_jutsu.years)),
            genres=", ".join([genre.name for genre in anime_jutsu.info.genres]),
            ongoing="✅ <b>Онгоинг:</b> Да" if anime_jutsu.ongoing else "❌ <b>Онгоинг:</b> Нет",
            episodes=anime_jutsu.content.count,
            rating=f"{anime_jikan["score"]}/10",
            description=anime_jutsu.description[:400],
            trailer=anime_jikan["trailer"]["url"],
            link=f"https://jut.su/{anime_id}/",
        ),
    )
