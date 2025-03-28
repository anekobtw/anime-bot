from typing import List

from aiogram import F, Router, exceptions, types
from aiogram.filters import Command
from anilibria import Anime

from enums import API, Buttons, GeneralMessage, StatusMessage
from handlers.helpers import generate_description

router = Router()


# Keyboards
def start_kb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=Buttons.RANDOM.value, callback_data="anime_random")],
            [types.InlineKeyboardButton(text=Buttons.TOP_GENRES.value, callback_data="top_genres")],
            [types.InlineKeyboardButton(text="📰 Телеграм канал с новостями", url="t.me/anekobtw_c")],
        ]
    )


def random_kb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=Buttons.RANDOM.value, callback_data="anime_random")],
            [types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")],
        ],
    )


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
@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    await message.answer(text=GeneralMessage.GREETING.value, reply_markup=start_kb())


@router.message(F.text)
async def _(message: types.Message) -> None:
    msg = await message.answer(StatusMessage.LOADING.value)
    await message.delete()

    animes = API.anilibria.value.search(message.text)
    if not animes:
        await msg.edit_text(StatusMessage.NOT_FOUND.value)
        return
    await msg.edit_text(text=StatusMessage.FOUND.value, reply_markup=anime_kb(animes))


@router.callback_query(F.data.startswith("anime_"))
async def _(callback: types.CallbackQuery) -> None:
    anime_id = callback.data.split("_")[1]

    MAX_RETRIES = 3

    for attempt in range(MAX_RETRIES):
        try:
            anime = (
                API.anilibria.value.random() if anime_id == "random" else API.anilibria.value.search_id(int(anime_id))
            )
            description = await generate_description(anime)
            break
        except Exception as e:
            print(e)
            if attempt == MAX_RETRIES - 1:
                await callback.answer("⚠️ Не получилось найти аниме. Пожалуйтса, попробуйте позже.", show_alert=True)
                raise e

    await callback.message.edit_media(
        media=types.InputMediaPhoto(media=anime.poster_original_url, caption=description),
        reply_markup=random_kb(),
    )


@router.callback_query(F.data == "home")
async def _(callback: types.CallbackQuery) -> None:
    try:
        await callback.message.edit_text(text=GeneralMessage.GREETING.value, reply_markup=start_kb())
    except exceptions.TelegramBadRequest:
        await callback.message.delete()
        await callback.message.answer(text=GeneralMessage.GREETING.value, reply_markup=start_kb())
