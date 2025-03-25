import random

from aiogram import F, Router, exceptions, types
from aiogram.filters import Command
from jutsu_api import Filter

from enums import API, AnimeGenres, Buttons, GeneralMessage, StatusMessage
from handlers.helpers import generate_description

router = Router()


# Keyboards
def start_kb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=Buttons.RANDOM.value, callback_data="anime_random")],
            [types.InlineKeyboardButton(text=Buttons.TOP_GENRES.value, callback_data="top_genres")],
        ]
    )


def home_kb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")]])


def top_genres() -> types.InlineKeyboardMarkup:
    genre_list = list(AnimeGenres)
    rows = [[types.InlineKeyboardButton(text=genre.value[0], callback_data=f"top_{genre.value[1]}") for genre in genre_list[i : i + 3]] for i in range(0, len(genre_list), 3)]
    rows.append([types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


def anime_kb(animes: list, k: int = None) -> types.InlineKeyboardMarkup:
    if k:
        animes = animes[:k]
    btns = [[types.InlineKeyboardButton(text=f"{anime.name.name}", callback_data=f"anime_{anime.name.id}") for anime in animes[i : i + 2]] for i in range(0, len(animes), 2)]
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

    animes = API.jutsu.value.search(message.text)
    if not animes:
        await msg.edit_text(StatusMessage.NOT_FOUND.value)
        return
    await msg.edit_text(text=StatusMessage.FOUND.value, reply_markup=anime_kb(animes))


@router.callback_query(F.data.startswith("anime_"))
async def _(callback: types.CallbackQuery) -> None:
    anime_id = callback.data.split("_")[1]

    if anime_id == "random":
        animes = None
        while not animes:
            animes = API.jutsu.value.search(filter=Filter(genres=[random.choice(Filter.available.genres)], types=[random.choice(Filter.available.types)], years=[random.choice(Filter.available.years)], sorting=[random.choice(Filter.available.sorting)]), maxpage=1)
        res = generate_description(random.choice(animes).name.id)
    else:
        res = generate_description(callback.data.split("_")[1])

    await callback.message.edit_media(media=types.InputMediaPhoto(media=res[0], caption=res[1]), reply_markup=home_kb())


@router.callback_query(F.data.startswith("top_"))
async def _(callback: types.CallbackQuery) -> None:
    link = f"{callback.data.split('_')[1]}/"
    if link == "genres/":
        await callback.message.edit_text(text=GeneralMessage.TOP_DESCRIPTION.value, reply_markup=top_genres())
        return
    else:
        animes = API.jutsu.value.search(filter=Filter(link=link), maxpage=1)
        await callback.message.edit_text(text=GeneralMessage.YOUR_TOP.value, reply_markup=anime_kb(animes, 10))


@router.callback_query(F.data == "home")
async def _(callback: types.CallbackQuery) -> None:
    try:
        await callback.message.edit_text(text=GeneralMessage.GREETING.value, reply_markup=start_kb())
    except exceptions.TelegramBadRequest:
        await callback.message.delete()
        await callback.message.answer(text=GeneralMessage.GREETING.value, reply_markup=start_kb())
