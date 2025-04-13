import datetime
from enum import Enum

from aiogram import types
from anilibria.client import AniLibriaClient, Anime
from jikanpy import Jikan
from jutsu_api import API


class Error(Enum):
    SERVER_ERROR = "⚠️ Сервер не отвечает. Пожалуйста, попробуйте позже."
    NOT_FOUND = "⚠️ Не получилось найти аниме. Пожалуйста, попробуйте позже."
    GENERAL_ERROR = "⚠️ Произошла ошибка. Пожалуйста, попробуйте позже."


class Buttons(Enum):
    RANDOM = "🎲 Случайное аниме"
    WATCH = "▶️ Смотреть"
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
            [types.InlineKeyboardButton(text=Buttons.SCHEDULE.value, callback_data=f"schedule_{datetime.datetime.now().weekday()}")],
            [types.InlineKeyboardButton(text=Buttons.TELEGRAM_CHANNEL.value, url="t.me/anekobtw_c")],
        ]
    )

    @staticmethod
    def anime_page(anime_id: int) -> types.InlineKeyboardMarkup:
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=Buttons.WATCH.value, callback_data=f"watch_{anime_id}"),
                    types.InlineKeyboardButton(text=Buttons.SIMILAR.value, callback_data=f"similar_{anime_id}"),
                ],
                [types.InlineKeyboardButton(text=Buttons.RANDOM.value, callback_data="anime_random")],
                [types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")],
            ]
        )

    @staticmethod
    def anime_search(animes: list[Anime], limit: int = None) -> types.InlineKeyboardMarkup:
        if limit:
            animes = animes[:limit]
        btns = [[types.InlineKeyboardButton(text=f"{anime.name_ru} ({len(anime.episodes)} серий)", callback_data=f"anime_{anime.id}")] for anime in animes]
        btns.append([types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")])
        return types.InlineKeyboardMarkup(inline_keyboard=btns)


class GeneralMessage(Enum):
    GREETING = "👋 Привет! Напиши название аниме, и я найду его для тебя!\n\n<b><i>Часто сервер анилибрии падает, из-за чего запросы могут не обрабатываться. В таком случае просто попробуйте снова позже.</i></b>"


class AnimeInfo(Enum):
    DESCRIPTION = "🍿 <code>{name}</code> ({year})\n\n" "❤️ <b>Понравилось:</b> {in_favorites}\n" "🎥 <b>Тип:</b> {type}\n" "🎭 <b>Жанры:</b> {genres}\n\n" "📃 <i>{description}</i>\n\n" "<b>@watch_animes_bot</b>"
    LINKS = "🎬 <b>Трейлер:</b>\n" '🇯🇵 <b><a href="{trailer}">YouTube</a></b>\n\n' "📺 <b>Смотреть:</b>\n" '🇷🇺 <b><a href="{anilibria}">AniLibria</a></b>\n' '🇷🇺 <b><a href="{jutsu}">Jutsu</a></b>\n\n' "📖 <b>Манга:</b>\n" "coming soon...\n\n"


class StatusMessage(Enum):
    SEARCHING = "⏳ Ищу аниме... Один момент!"
    NOT_FOUND = "😞 Упс! Аниме не найдено. Попробуй другое название!"
    FOUND = "🔎 Вот что я нашел:"


class API(Enum):
    anilibria = AniLibriaClient()
    jikan = Jikan()
    jutsu = API()
