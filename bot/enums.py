import datetime
from enum import Enum

from aiogram import types
from anilibria.client import AniLibriaClient
from jikanpy import Jikan


class Error(Enum):
    SERVER_ERROR = "⚠️ Сервер не отвечает. Пожалуйста, попробуйте позже."
    NOT_FOUND = "⚠️ Не получилось найти аниме. Пожалуйста, попробуйте позже."
    GENERAL_ERROR = "⚠️ Произошла ошибка. Пожалуйста, попробуйте позже."


class Buttons(Enum):
    RANDOM = "🎲 Случайное аниме"
    SCHEDULE = "📅 Расписание"
    SIMILAR = "🔍 Похожие аниме"
    HOME = "🏠 На главную"
    TELEGRAM_CHANNEL = "📰 Телеграм канал с новостями"


class Keyboards(Enum):
    SCHEDULE = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Пн", callback_data="schedule_0"),
                types.InlineKeyboardButton(text="Вт", callback_data="schedule_1"),
                types.InlineKeyboardButton(text="Ср", callback_data="schedule_2"),
                types.InlineKeyboardButton(text="Чт", callback_data="schedule_3"),
                types.InlineKeyboardButton(text="Пт", callback_data="schedule_4"),
                types.InlineKeyboardButton(text="Сб", callback_data="schedule_5"),
                types.InlineKeyboardButton(text="Вс", callback_data="schedule_6"),
            ],
            [types.InlineKeyboardButton(text="📅 Последние добавленные релизы", callback_data="updates")],
            [types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")],
        ]
    )
    MENU = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=Buttons.RANDOM.value, callback_data="anime_random")],
            [
                types.InlineKeyboardButton(
                    text=Buttons.SCHEDULE.value, callback_data=f"schedule_{datetime.datetime.today().weekday()}"
                )
            ],
            [types.InlineKeyboardButton(text=Buttons.TELEGRAM_CHANNEL.value, url="t.me/anekobtw_c")],
        ]
    )

    @staticmethod
    def anime(anime_id: int) -> types.InlineKeyboardMarkup:
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text=Buttons.RANDOM.value, callback_data="anime_random")],
                [types.InlineKeyboardButton(text=Buttons.SIMILAR.value, callback_data=f"similar_{anime_id}")],
                [types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")],
            ]
        )


class GeneralMessage(Enum):
    GREETING = "👋 Привет! Напиши название аниме, и я найду его для тебя!\n\n<b><i>Часто сервер анилибрии падает, из-за чего запросы могут не обрабатываться. В таком случае просто попробуйте снова позже.</i></b>"


class AnimeInfo(Enum):
    DESCRIPTION = (
        "🍿 <code>{name}</code> ({year}, {status})\n\n"
        "⭐ <b>Оценка</b> {rating}/10\n"
        "❤️ <b>Понравилось:</b> {in_favorites}\n"
        "🎥 <b>Тип:</b> {type}\n"
        "🎭 <b>Жанры:</b> {genres}\n\n"
        "📝 <i>{description}</i>\n\n"
        "▶️ <b><a href='{trailer}'>Трейлер</a></b> | 📺 <b><a href='{link_anilibria}'>AniLibria</a></b>\n\n"
        "<b>@watch_animes_bot</b>"
    )


class StatusMessage(Enum):
    LOADING = "⏳ Ищу аниме... Один момент!"
    NOT_FOUND = "😞 Упс! Аниме не найдено. Попробуй другое название!"
    FOUND = "🔎 Вот что я нашел:"


class API(Enum):
    anilibria = AniLibriaClient()
    jikan = Jikan()
