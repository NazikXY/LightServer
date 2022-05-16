from fastapi import APIRouter, Depends, Body

from LightServer import models
from LightServer.services.auth import get_current_user
from LightServer.services.search import SearchService

router = APIRouter(
    prefix="/search",
    tags=["search"]
)


@router.post("/by_login", response_model=models.User)
async def get_user_by_login(
        login: str = Body(..., example='some_user_login'),
        user: models.User = Depends(get_current_user),
        search_service: SearchService = Depends()
):
    return search_service.by_login(login)