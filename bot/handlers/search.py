from itertools import combinations

from aiogram import F, Router, exceptions, types
from aiogram.filters import Command
from anilibria.exceptions import AniLibriaRequestException
from anilibria.models import SearchFilter

from enums import API, Error, GeneralMessage, Keyboards, StatusMessage
from handlers.helpers import generate_description, generate_links

router = Router()


# Handlers
@router.message(F.text, Command("start", "menu"))
async def start(message: types.Message) -> None:
    await message.answer(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)


@router.message(F.text)
async def _(message: types.Message) -> None:
    msg = await message.answer(StatusMessage.SEARCHING.value)
    await message.delete()

    try:
        animes = API.anilibria.value.search(message.text)
    except AniLibriaRequestException:
        await msg.edit_text(Error.SERVER_ERROR.value)
        return

    if not animes:
        await msg.edit_text(StatusMessage.NOT_FOUND.value)
        return
    await msg.edit_text(text=StatusMessage.FOUND.value, reply_markup=Keyboards.anime_search(animes))


@router.callback_query(F.data.startswith("anime_"))
async def search_anime(callback: types.CallbackQuery) -> None:
    data = callback.data.split("_")[1]

    try:
        anime = API.anilibria.value.random(
        ) if data == "random" else API.anilibria.value.search_id(int(data))
        description = generate_description(anime)
    except AniLibriaRequestException:
        await callback.answer(Error.SERVER_ERROR.value, show_alert=True)
        return
    except Exception as e:
        print(e)
        await callback.answer(Error.NOT_FOUND.value, show_alert=True)
        return

    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=anime.poster_original_url, caption=description),
        reply_markup=Keyboards.anime_page(anime.id),
    )


@router.callback_query(F.data.startswith("similar_"))
async def similar(callback: types.CallbackQuery) -> None:
    anime_id = callback.data.split("_")[1]
    try:
        anime = API.anilibria.value.search_id(anime_id)
    except AniLibriaRequestException:
        await callback.answer(Error.SERVER_ERROR.value, show_alert=True)
        return

    msg = await callback.message.answer("<b>⌛ Поиск..</b>")
    animes = []
    all_genre_pairs = [combinations(anime.genres, i)
                       for i in range(min(5, len(anime.genres)), 1, -1)]

    for combination in all_genre_pairs:
        for pair in combination:
            results = API.anilibria.value.search(filter=SearchFilter(
                years=list(range(anime.year - 2, anime.year + 3)), genres=list(pair)))
            for result in results:
                if result.id != anime.id and result not in animes:
                    animes.append(result)

            if len(animes) >= 5:
                break

        if len(animes) >= 5:
            break

    await msg.edit_text(f"<b>Похожие аниме на <i>{anime.name_ru}</i></b>", reply_markup=Keyboards.anime_search(animes[:5]))


@router.callback_query(F.data.startswith("watch_"))
async def _(callback: types.CallbackQuery) -> None:
    try:
        _, anime_id = callback.data.split("_")
        await callback.message.answer(text=StatusMessage.FOUND.value, reply_markup=generate_links(anime_id))
    except AniLibriaRequestException:
        await callback.answer(Error.SERVER_ERROR.value, show_alert=True)
    except Exception as e:
        print(e)
        await callback.answer(Error.GENERAL_ERROR.value, show_alert=True)


@router.callback_query(F.data == "home")
async def home(callback: types.CallbackQuery) -> None:
    try:
        await callback.message.edit_text(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)
    except exceptions.TelegramBadRequest:
        await callback.message.delete()
        await callback.message.answer(text=GeneralMessage.GREETING.value, reply_markup=Keyboards.MENU.value)
