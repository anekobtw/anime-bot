from aiogram import F, Router, types

from enums import API, Keyboards
from handlers.helpers import get_relative_time
from anilibria.exceptions import AniLibriaRequestException
from enums import Error

router = Router()


@router.callback_query(F.data.startswith("schedule_"))
async def _(callback: types.CallbackQuery) -> None:
    try:
        _, day = callback.data.split("_")
        animes = API.anilibria.value.schedule(int(day))
        text = f"📅 <b>Календарь релизов. День {int(day)+1} из 7.</b>\n\n"
        for anime in animes:
            text += f"<code>{anime.name_ru}</code>\n<i>вышло {get_relative_time(anime.last_change)}</i>\n\n"
        await callback.message.edit_text(text=text, reply_markup=Keyboards.SCHEDULE.value)
    except AniLibriaRequestException:
        await callback.answer(Error.SERVER_ERROR.value, show_alert=True)
    except Exception:
        await callback.answer(Error.NOT_FOUND.value, show_alert=True)


@router.callback_query(F.data == "updates")
async def _(callback: types.CallbackQuery) -> None:
    try:
        animes = API.anilibria.value.updates()
        text = f"📅 <b>Последние добавленные релизы</b>\n\n"
        for anime in animes:
            text += f"<code>{anime.name_ru}</code>\n<i>вышло {get_relative_time(anime.last_change)}</i>\n\n"
        await callback.message.edit_text(text=text, reply_markup=Keyboards.SCHEDULE.value)
    except AniLibriaRequestException:
        await callback.answer(Error.SERVER_ERROR.value, show_alert=True)
    except Exception:
        await callback.answer(Error.NOT_FOUND.value, show_alert=True)

