import os
from aiogram import F, Router, types
import tracemoepy
from nekosbest import Client

router = Router()


@router.message(F.text.startswith("https://"))
async def _(message: types.Message):
    try:
        async with tracemoepy.AsyncTrace() as tracemoe:
            resp = await tracemoe.search(message.text, is_url=True)
            video = await tracemoe.natural_preview(resp)

            with open(f'{message.from_user.id}.mp4', 'wb') as f:
                f.write(video)
                await message.answer_video(video=types.FSInputFile(f.name), caption=f"🤔 It's probably from anime <b>{resp.result[0].anilist.title.romaji}</b>\Similarity: <b>{round(resp.result[0].similarity*100, 1)}%</b>")
            
            os.remove(f'{message.from_user.id}.mp4')

    except tracemoepy.EmptyImage:
        await message.answer("⚠️ No image found in the link.")

    except tracemoepy.ServerError:
        await message.answer("⚠️ The image is malformed or something went wrong.")


@router.callback_query(F.data.startswith("image"))
async def _(callback: types.CallbackQuery) -> None:
    client = Client()
    result = await client.get_image(callback.data.split("_")[1], 1)
    await callback.message.edit_media(
        media=types.InputMediaPhoto(media=types.URLInputFile(result.url),
        caption=f"by <b>{result.artist_name}</b>"),
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(text="🎴 Random female", callback_data="image_waifu"),
            types.InlineKeyboardButton(text="🎴 Random male", callback_data="image_husbando")
            ]]
        )
    )
