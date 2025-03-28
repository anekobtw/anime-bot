from enum import Enum

from anilibria import AniLibriaClient
from jikanpy import Jikan
from jutsu_api import API


class Buttons(Enum):
    RANDOM = "🎲 Рандомное аниме"
    TOP_GENRES = "🏆 Топ по жанрам"
    HOME = "🏠 На главную"


class GeneralMessage(Enum):
    GREETING = "👋 Привет! Напиши название аниме, и я найду его для тебя!"
    YOUR_TOP = '<b>Ваш топ аниме:</b>\nВот подборка аниме, которые могут вам понравиться, основываясь на выбранных жанрах и периодах. Нажмите на кнопки ниже, чтобы узнать больше о каждом тайтле.\n\nЕсли что-то не так или хотите изменить критерии, вернитесь на главную страницу через кнопку "Домой" и попробуйте снова. Приятного просмотра! 😊'
    TOP_DESCRIPTION = f"<b>{Buttons.TOP_GENRES.value}</b>\n\nИсследуйте разнообразие жанров аниме — от захватывающих приключений и фантастики до трогательной романтики и повседневности. Выберите жанр, чтобы увидеть лучшие тайтлы, которые подойдут именно вам."


class AnimeInfo(Enum):
    DESCRIPTION = (
        "🍿 <b>{name_ru} ({year})</b>\n"
        "⭐ <b>Оценка:</b> {rating}/10\n"
        "❤️ <b>Понравилось:</b> {in_favorites}\n\n"
        "🎭 <b>Жанры:</b> {genres}\n"
        "🏷️ <b>Статус:</b> {status}\n"
        "📊 <b>Эпизоды:</b> {episodes} (каждая по {episodes_length} мин)\n\n"
        "📝 <i>{description}</i>\n\n"
        "▶️ <b><a href='{trailer}'>Смотреть трейлер</a></b>\n"
        "📺 <b><a href='{link_anilibria}'>Смотреть на AniLibria</a></b>\n"
        "📺 <b><a href='{link_jutsu}'>Смотреть на jut.su</a></b>\n\n"
        "<b>@watch_animes_bot</b>"
    )


class StatusMessage(Enum):
    LOADING = "⏳ Ищу аниме... Один момент!"
    NOT_FOUND = "😞 Упс! Аниме не найдено. Попробуй другое название!"
    FOUND = "🔎 Вот что я нашел:"


class API(Enum):
    jutsu = API()
    anilibria = AniLibriaClient()
    jikan = Jikan()
