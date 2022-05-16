from typing import List

from fastapi import APIRouter, Header, Depends, Response, status, Body
from LightServer import models
from LightServer.services.auth import get_current_user
from LightServer.services.friends import FriendsService

router = APIRouter(
    prefix="/friends",
    tags=["friends"],
)


@router.get("/list", response_model=List[models.User])
async def get_friends(
        user: models.User = Depends(get_current_user),
        friends_service: FriendsService = Depends()
):
    return friends_service.get_list(user)


@router.post("/add", status_code=status.HTTP_202_ACCEPTED)
async def add_friend(
        another_user_id: int,
        user: models.User = Depends(get_current_user),
        friends_service: FriendsService = Depends()
):
    friends_service.add_friend(user, another_user_id)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/del", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend(
        another_user_id: int = Body(...),
        user: models.User = Depends(get_current_user),
        friends_service: FriendsService = Depends()
):
    friends_service.remove_friend(user, another_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
