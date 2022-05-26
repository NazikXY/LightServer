from fastapi import APIRouter

from . import (
    auth,
    search,
    friends,
    dialogs,
    messages,
    posts,
)


router = APIRouter()
router.include_router(auth.router)
router.include_router(search.router)
router.include_router(friends.router)
router.include_router(dialogs.router)
router.include_router(messages.router)
router.include_router(posts.router)

