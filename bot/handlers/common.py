import random

from aiogram import F, Router, types
from aiogram.filters import Command
from jutsu_api import Filter

from enums import API, Buttons, GeneralMessage, StatusMessage
from handlers.helpers import generate_description

router = Router()


def start_kb() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=Buttons.RANDOM.value)], [types.KeyboardButton(text=Buttons.TOP_YEARS.value), types.KeyboardButton(text=Buttons.TOP_GENRES.value), types.KeyboardButton(text=Buttons.TOP_TYPES.value)]], resize_keyboard=True)


def top_kb(array: list) -> types.InlineKeyboardMarkup:
    rows = [[types.InlineKeyboardButton(text=y.name, callback_data=f"top_{y.id}") for y in array[i : i + 3]] for i in range(0, len(array), 3)]
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    await message.answer(text=GeneralMessage.GREETING.value, reply_markup=start_kb())


@router.message(F.text)
async def _(message: types.Message) -> None:
    msg = await message.answer(StatusMessage.LOADING.value)
    await message.delete()

    match message.text:
        case Buttons.RANDOM.value:
            animes = None
            while not animes:
                animes = API.jutsu.value.search(filter=Filter(genres=[random.choice(Filter.available.genres)], types=[random.choice(Filter.available.types)]), maxpage=1)
            res = generate_description(random.choice(animes).name.id)
            await message.answer_photo(res[0], res[1])
            await msg.delete()
            return

        case Buttons.TOP_YEARS.value:
            # animes = API.jutsu.value.search(filter=Filter(link="ongoing/"), maxpage=1)[:5]
            await msg.edit_text(text=Buttons.TOP_YEARS.value, reply_markup=top_kb(Filter.available.years))
            return

        case Buttons.TOP_GENRES.value:
            await msg.edit_text(text=Buttons.TOP_GENRES.value, reply_markup=top_kb(Filter.available.genres))
            return

        case Buttons.TOP_TYPES.value:
            await msg.edit_text(text=Buttons.TOP_TYPES.value, reply_markup=top_kb(Filter.available.types))
            return

        case _:
            animes = API.jutsu.value.search(message.text)
            if not animes:
                await msg.edit_text(StatusMessage.NOT_FOUND.value)
                return

    btns = [[types.InlineKeyboardButton(text=f"{anime.name.name} ({anime.content.count} серий)", callback_data=f"anime_{anime.name.id}")] for anime in animes]
    await msg.edit_text(text=StatusMessage.FOUND.value, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=btns))


@router.callback_query(F.data.startswith("anime_"))
async def _(callback: types.CallbackQuery) -> None:
    res = generate_description(callback.data.split("_")[1])
    await callback.message.answer_photo(res[0], res[1])
    await callback.message.delete()


# Anime recommendations
#
