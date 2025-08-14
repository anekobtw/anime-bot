from aiogram import F, Router, types
import requests

router = Router()

API_URL = 'https://graphql.anilist.co'

SEARCH_QUERY = '''
query ($search: String) {
  Page {
    media(search: $search, type: ANIME) {
      id
      title {
        english
      }
    }
  }
}
'''

ANIME_QUERY = '''
query ($id: Int) {
  Media (id: $id, type: ANIME) {
    id
    title {
      english
    }
    format
    description
    startDate {
        year
        month
        day
    }
    endDate {
        year
        month
        day
    }
    episodes
    duration
    trailer {
        id
        site
    }
    coverImage {
        extraLarge
    }
    genres
    averageScore
    favourites
    isAdult
  }
}
'''


@router.message()
async def search_anime(message: types.Message):
    response = requests.post(API_URL, json={'query': SEARCH_QUERY, 'variables': {'search': message.text}})
    data = response.json()

    if "errors" in data:
        await callback.answer(data["errors"][0]["message"])
        return

    media_list = data.get("data", {}).get("Page", {}).get("media", [])
    
    buttons = []
    for anime in media_list[:5]:
        title = anime.get("title", {}).get("english")
        if title:
            buttons.append([types.InlineKeyboardButton(text=title, callback_data=f'anime_{anime["id"]}')])

    if buttons:
        await message.answer("<b>Here is what I found</b>", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))
    else:
        await message.answer("Anime not found.")


@router.callback_query(F.data.startswith("anime_"))
async def search_particular_anime(callback: types.CallbackQuery):
    response = requests.post(API_URL, json={'query': ANIME_QUERY, 'variables': {"id": int(callback.data.split("_")[1])}})
    data = response.json()

    if "errors" in data:
        await callback.answer(data["errors"][0]["message"])
        return

    media = data.get("data", {}).get("Media", {})

    title = media.get("title", "").get("english", "")
    form = media.get("format", "")
    description = media.get("description", "").replace("<br>", "")
    _startDate = media.get("startDate", {})
    startDate = f"{_startDate.get("day", None)}/{_startDate.get("month", None)}/{_startDate.get("year", None)}"
    _endDate = media.get("endDate", {})
    endDate = f"{_endDate.get("day", None)}/{_endDate.get("month", None)}/{_endDate.get("year", None)}"
    episodes = media.get("episodes", None)
    duration = media.get("duration", None)
    coverImage = media.get("coverImage", {}).get("extraLarge", "")
    genres = media.get("genres", [])
    averageScore = media.get("averageScore", "")
    favorites = media.get("favourites", "")
    isAdult = media.get("isAdult", False)

    print(data)

    scoreText = f"{round(averageScore * 0.1, 1)} / 10".ljust(15)
    episodesText = f"{episodes} eps".ljust(15)

    caption = f"""
🍿 <code>{title}</code> {"\n<b>🔞 THIS ANIME IS MARKED 18+</b>\n" if isAdult else ""}
<i>{startDate} - {endDate}</i>

<b>⭐  {scoreText}❤️  {favorites}</b>
<b>🎬  {episodesText}⏱️  {duration} min</b>
<b>🎭  {" · ".join(genres)}</b>

{description}
"""

    if len(caption) > 1024:
      cap1, cap2 = caption[:1024], caption[1024:]
      await callback.message.answer_photo(photo=types.URLInputFile(coverImage), caption=cap1)
      await callback.message.answer(text=cap2)
    else:
      await callback.message.answer_photo(photo=types.URLInputFile(coverImage), caption=caption)
# <b>🎞  {form}, {episodes} episodes, {duration} mins</b>