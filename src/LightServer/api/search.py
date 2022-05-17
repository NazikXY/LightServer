from fastapi import APIRouter, Depends, Body

from .. import models
from ..services.auth import get_current_user
from ..services.search import SearchService

router = APIRouter(
    prefix="/search",
    tags=["search"]
)


@router.post("/by_login", response_model=models.User, dependencies=[Depends(get_current_user)])
async def get_user_by_login(
        login: str = Body(..., example='some_user_login'),
        search_service: SearchService = Depends()
):
    return search_service.by_login(login)