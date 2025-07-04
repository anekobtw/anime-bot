from aiogram import F, Router, exceptions, types
from aiogram.filters import Command

from enums import API, Error, Keyboards, StatusMessage

router = Router()


@router.message(F.text, Command("start", "menu"))
async def start(message: types.Message) -> None:
    kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="🎲 Random anime", callback_data="anime_random")],
                [
                    types.InlineKeyboardButton(text="🎴 Random female", callback_data="image_waifu"),
                    types.InlineKeyboardButton(text="🎴 Random male", callback_data="image_husbando"),
                ],
                [types.InlineKeyboardButton(text="📃 Third-Party Services", callback_data="third-party")],
                [types.InlineKeyboardButton(text="📰 Telegram channel with news", url="t.me/anekobtw_c")],
            ]
        )

    await message.answer(text=f"👋 Hi, {message.from_user.username}! Send me the anime name and I'll find it for you!", reply_markup=kb)
