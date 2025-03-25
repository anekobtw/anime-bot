from enums import API, AnimeInfo


def generate_description(anime_id: str) -> list[str, str]:
    jutsu = API.jutsu.value.anime(anime_id)
    jikan = API.jikan.value.search(search_type="anime", query=jutsu.name.orig)["data"][0]

    return (
        jikan["images"]["jpg"]["large_image_url"],
        "".join(AnimeInfo.DESCRIPTION.value).format(
            emoji="🔞" if jutsu.age >= 18 else "🍿",
            name=jutsu.name.name,
            years=", ".join(map(str, jutsu.years)),
            genres=", ".join([genre.name for genre in jutsu.info.genres + jutsu.info.types]),
            ongoing="✅ <b>Онгоинг:</b> Да" if jutsu.ongoing else "❌ <b>Онгоинг:</b> Нет",
            episodes=jutsu.content.count,
            rating=f"{jikan["score"]}/10",
            description=f"{jutsu.description[:200]}...Читать полностью",
            trailer=jikan["trailer"]["url"],
            link=f"https://jut.su/{anime_id}/",
        ),
    )
