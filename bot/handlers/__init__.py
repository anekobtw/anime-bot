from aiogram import Router

from . import schedule, search

router = Router()
router.include_router(search.router)
router.include_router(schedule.router)
