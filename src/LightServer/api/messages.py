from fastapi import (
    APIRouter,
    Depends,
    Body,
    status,
    Response
)

from LightServer import models
from LightServer.services.auth import get_current_user
from LightServer.services.messages import MessageService

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


@router.post("/send", response_model=models.Message, status_code=status.HTTP_201_CREATED)
async def send_message(
        message: models.MessageCreate = Body(...),
        user: models.User = Depends(get_current_user),
        message_service: MessageService = Depends()
):
    return message_service.send_message(user, message=message)


@router.patch("/edit", response_model=models.Message, status_code=status.HTTP_202_ACCEPTED)
async def edit_message(
        message: models.MessageUpdate = Body(...),
        user: models.User = Depends(get_current_user),
        message_service: MessageService = Depends()
):
    return message_service.edit_message(user, message=message)


@router.post("/forward", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def forward_message(
    message_forward: models.MessageForward = Body(...),
    user: models.User = Depends(get_current_user),
    message_service: MessageService = Depends()
):
    ...


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def forward_message(
    message_id: int = Body(...),
    user: models.User = Depends(get_current_user),
    message_service: MessageService = Depends()
):
    message_service.delete_message(user, message_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
