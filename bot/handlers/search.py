from itertools import combinations
from typing import List

from aiogram import F, Router, exceptions, types
from aiogram.filters import Command
from anilibria.exceptions import AniLibriaRequestException
from anilibria.models import Anime, SearchFilter

from enums import API, Buttons, Error, GeneralMessage, Keyboards, StatusMessage
from handlers.helpers import generate_description

router = Router()


# Keyboards
def anime_kb(animes: List[Anime], k: int = None) -> types.InlineKeyboardMarkup:
    if k:
        animes = animes[:k]
    btns = [
        [
            types.InlineKeyboardButton(
                text=f"{anime.name_ru} ({anime.episodes_count} серий)", callback_data=f"anime_{anime.id}"
            )
        ]
        for anime in animes
    ]
    btns.append([types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")])
    return types.InlineKeyboardMarkup(inline_keyboard=btns)


# Handlers
@router.message(F.text, Command("start", "menu"))
async def start(message: types.Message) -> None:
    await message.answer(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)


@router.message(F.text)
async def handle_text(message: types.Message) -> None:
    msg = await message.answer(StatusMessage.LOADING.value)
    await message.delete()

    animes = API.anilibria.value.search(message.text)
    if not animes:
        await msg.edit_text(StatusMessage.NOT_FOUND.value)
        return
    await msg.edit_text(text=StatusMessage.FOUND.value, reply_markup=anime_kb(animes))


@router.callback_query(F.data.startswith("anime_"))
async def search_anime(callback: types.CallbackQuery) -> None:
    data = callback.data.split("_")[1]

    try:
        anime = API.anilibria.value.random() if data == "random" else API.anilibria.value.search_id(int(data))
        description = await generate_description(anime)
    except AniLibriaRequestException:
        await callback.answer(Error.SERVER_ERROR.value, show_alert=True)
    except Exception:
        await callback.answer(Error.NOT_FOUND.value, show_alert=True)

    await callback.message.edit_media(
        media=types.InputMediaPhoto(media=anime.poster_original_url, caption=description),
        reply_markup=Keyboards.anime(anime.id),
    )


@router.callback_query(F.data.startswith("similar_"))
async def similar(callback: types.CallbackQuery) -> None:
    anime_id = callback.data.split("_")[1]
    anime = API.anilibria.value.search_id(anime_id)
    genre_pairs = list(combinations(anime.genres, 2))

    msg = await callback.message.answer(f"<b>⌛ Поиск.. 0%</b>")
    animes = []

    for idx, pair in enumerate(genre_pairs, start=1):
        results = API.anilibria.value.search(
            filter=SearchFilter(
                years=list(range(anime.year - 2, anime.year + 3)),
                genres=pair,
                limit=3,
            )
        )

        for result in results:
            if result.id != anime.id and result not in animes:
                animes.append(result)

        await msg.edit_text(f"<b>{'⌛' if idx % 2 == 0 else '⏳'} Поиск.. {round(idx/len(genre_pairs)*100, 1)}%</b>")

    await msg.edit_text(f"<b>Похожие аниме на <i>{anime.name_ru}</i></b>", reply_markup=anime_kb(animes))


@router.callback_query(F.data == "home")
async def home(callback: types.CallbackQuery) -> None:
    try:
        await callback.message.edit_text(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)
    except exceptions.TelegramBadRequest:
        await callback.message.delete()
        await callback.message.answer(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)
