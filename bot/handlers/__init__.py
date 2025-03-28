from aiogram import Router

from . import search

router = Router()
router.include_router(search.router)
