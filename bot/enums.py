from enum import Enum

from jikanpy import Jikan
from jutsu_api import API


class GeneralMessage(Enum):
    GREETING = "👋 Привет! Напиши название аниме, и я найду его для тебя!"
    YOUR_TOP = '<b>Ваш топ аниме:</b>\nВот подборка аниме, которые могут вам понравиться, основываясь на выбранных жанрах и периодах. Нажмите на кнопки ниже, чтобы узнать больше о каждом тайтле.\n\nЕсли что-то не так или хотите изменить критерии, вернитесь на главную страницу через кнопку "Домой" и попробуйте снова. Приятного просмотра! 😊'
    TOP_DESCRIPTION = "<b>{emoji} {name}</b> ({years}) • {rating}\n\n" "✍️ <b>Тип:</b> {types}\n" "🎭 <b>Жанр:</b> {genres}\n" "{ongoing}\n" "📊 <b>Эпизоды:</b> {episodes}\n\n" "📝 <i>{description}...</i>\n\n" "▶️ <a href='{trailer}'>Смотреть трейлер</a>\n" "📺 <a href='{link}'>Смотреть аниме</a>"  # noqa: E501


class StatusMessage(Enum):
    LOADING = "⏳ Ищу аниме... Один момент!"
    NOT_FOUND = "😞 Упс! Аниме не найдено. Попробуй другое название!"
    FOUND = "🔎 Вот что я нашел:"


class Buttons(Enum):
    RANDOM = "🍀 Рандомное аниме"
    TOP_GENRES = "🏆 Топ по жанрам"
    HOME = "🏠 На главную"


class TopCategoryDesc(Enum):
    GENRES = f"<b>{Buttons.TOP_GENRES.value}</b>\n\nИсследуйте разнообразие жанров аниме — от захватывающих приключений и фантастики до трогательной романтики и повседневности. Выберите жанр, чтобы увидеть лучшие тайтлы, которые подойдут именно вам."


class AnimeGenres(Enum):
    ONGOING = ("Онгоинг", "ongoing")
    YEAR2025 = ("2025", "2025")
    YEAR2024 = ("2024", "2024")
    YEAR2023 = ("2023", "2023")
    YEAR2022 = ("2022", "2022")
    YEARS20152021 = ("2015-2021", "2015-2021")
    YEARS20082014 = ("2008-2014", "2008-2014")
    YEARS20002007 = ("2000-2007", "2000-2007")
    BEFORE_2000 = ("До 2000", "before2000")
    MYSTIC = ("Мистика", "mystic")
    EVERYDAY = ("Повседневность", "everyday")
    FANTASY = ("Фэнтези", "fantasy")
    COMEDY = ("Комедия", "comedy")
    ROMANCE = ("Романтика", "romance")
    FANTASTIC = ("Фантастика", "fantastic")
    ADVENTURE = ("Приключения", "adventure")
    DETECTIVE = ("Детектив", "detective")
    THRILLER = ("Триллер", "thriller")
    DRAMA = ("Драма", "drama")
    PSYCHOLOGY = ("Психология", "psychology")
    ACTION = ("Боевик", "action")
    FIGHTING = ("Боевые искусства", "fighting")
    VAMPIRE = ("Вампиры", "vampire")
    MILITARY = ("Военное", "military")
    DEMONS = ("Демоны", "demons")
    GAME = ("Игры", "game")
    HISTORICAL = ("История", "historical")
    SPACE = ("Космос", "space")
    MAGIC = ("Магия", "magic")
    MECHA = ("Меха", "mecha")
    MUSIC = ("Музыка", "music")
    PARODY = ("Пародия", "parody")
    POLICE = ("Полиция", "police")
    SAMURAI = ("Самураи", "samurai")
    SHOJO = ("Сёдзё", "shojo")
    SHONEN = ("Сёнен", "shonen")
    SPORT = ("Спорт", "sport")
    SUPERPOWER = ("Суперсила", "superpower")
    HORROR = ("Ужасы", "horror")
    SCHOOL = ("Школа", "school")


class API(Enum):
    jutsu = API()
    jikan = Jikan()
