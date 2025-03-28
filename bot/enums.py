import datetime
from enum import Enum

from aiogram import types
from anilibria import AniLibriaClient
from jikanpy import Jikan
from jutsu_api import API


class Buttons(Enum):
    RANDOM = "🎲 Рандомное аниме"
    SCHEDULE = "📅 Расписание"
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
    RANDOM = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=Buttons.RANDOM.value, callback_data="anime_random")],
            [types.InlineKeyboardButton(text=Buttons.HOME.value, callback_data="home")],
        ],
    )


class GeneralMessage(Enum):
    GREETING = "👋 Привет! Напиши название аниме, и я найду его для тебя!"
    YOUR_TOP = '<b>Ваш топ аниме:</b>\nВот подборка аниме, которые могут вам понравиться, основываясь на выбранных жанрах и периодах. Нажмите на кнопки ниже, чтобы узнать больше о каждом тайтле.\n\nЕсли что-то не так или хотите изменить критерии, вернитесь на главную страницу через кнопку "Домой" и попробуйте снова. Приятного просмотра! 😊'
    TOP_DESCRIPTION = f"Исследуйте разнообразие жанров аниме — от захватывающих приключений и фантастики до трогательной романтики и повседневности. Выберите жанр, чтобы увидеть лучшие тайтлы, которые подойдут именно вам."


class AnimeInfo(Enum):
    DESCRIPTION = (
        "🍿 <code>{name}</code> ({year}, {status}{age})\n\n"
        "⭐ <b>Оценка</b> {rating}/10\n"
        "❤️ <b>Понравилось:</b> {in_favorites}\n"
        "🎥 <b>Тип:</b> {type}\n"
        "🎭 <b>Жанры:</b> {genres}\n\n"
        "📝 <i>{description}</i>\n\n"
        "▶️ <b><a href='{trailer}'>Трейлер</a></b> | 📺 <b><a href='{link_anilibria}'>AniLibria</a></b> | 📺 <b><a href='{link_jutsu}'>jut.su</a></b>\n\n"
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
