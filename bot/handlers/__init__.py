from aiogram import Router

from . import images, start, anime

router = Router()
router.include_router(start.router)
router.include_router(images.router)
router.include_router(anime.router)
