from enum import Enum

from jikanpy import Jikan
from jutsu_api import API


class GeneralMessage(Enum):
    GREETING = "👋 Привет! Напиши название аниме, и я найду его для тебя!"


class StatusMessage(Enum):
    LOADING = "⏳ Ищу аниме... Один момент!"
    NOT_FOUND = "😞 Упс! Аниме не найдено. Попробуй другое название!"
    FOUND = "🔎 Вот что я нашел:"


class AnimeInfo(Enum):
    DESCRIPTION = "<b>{emoji} {name} ({years}) • {rating}</b>\n\n" "✍️ {types}\n" "🎭 {genres}\n" "{ongoing}\n" "📊 Эпизоды: {episodes}\n\n" "📝 <i>{description}...</i>\n\n" "▶️ <a href='{trailer}'>Смотреть трейлер</a>\n" "📺 <a href='{link}'>Смотреть аниме</a>"  # noqa: E501


class Buttons(Enum):
    RANDOM = "🍀 Рандомное аниме"
    TOP_YEARS = "🏆 Топ по годам"
    TOP_GENRES = "🎭 Топ по жанрам"
    TOP_TYPES = "✍️ Топ по типам"


class API(Enum):
    jutsu = API()
    jikan = Jikan()
