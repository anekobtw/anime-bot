from typing import List

from aiogram import F, Router, exceptions, types
from aiogram.filters import Command
from anilibria import Anime
from anilibria import AniLibriaRequestException

from enums import API, Buttons, GeneralMessage, Keyboards, StatusMessage
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
@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None:
    await message.answer(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)


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

    try:
        anime = API.anilibria.value.random() if anime_id == "random" else API.anilibria.value.search_id(int(anime_id))
        description = await generate_description(anime)
    except AniLibriaRequestException:
        await callback.answer("⚠️ Сервер не отвечает. Пожалуйста, попробуйте позже.", show_alert=True)
    except Exception as e:
        print(e)
        await callback.answer("⚠️ Не получилось найти аниме. Пожалуйста, попробуйте позже.", show_alert=True)
        raise e

    await callback.message.edit_media(
        media=types.InputMediaPhoto(media=anime.poster_original_url, caption=description),
        reply_markup=Keyboards.RANDOM.value,
    )


@router.callback_query(F.data == "home")
async def _(callback: types.CallbackQuery) -> None:
    try:
        await callback.message.edit_text(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)
    except exceptions.TelegramBadRequest:
        await callback.message.delete()
        await callback.message.answer(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)
