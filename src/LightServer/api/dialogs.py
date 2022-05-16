from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status, Body
from LightServer import models
from LightServer.services.auth import get_current_user
from LightServer.services.dialogs import DialogService

router = APIRouter(
    prefix="/dialogs",
    tags=["dialogs"],
)


@router.get("/list", response_model=List[models.Dialog])
async def get_dialogs(
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    return dialog_service.get_list(user)


@router.post("/create", response_model=models.Dialog, status_code=status.HTTP_201_CREATED)
def add_member(
        new_dialog: models.DialogCreate = Body(...),
        member_ids: Optional[List[int]] = Body(...),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    return dialog_service.create(user, new_dialog, member_ids)


@router.get("/dialog_members", response_model=List[models.User])
def get_members(
        dialog_id: int,
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    return dialog_service.get_members(user, dialog_id)


@router.get("/dialog_messages", response_model=List[models.Message])
def get_messages(
        dialog_id: int,
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    return dialog_service.get_messages(user, dialog_id)


@router.post("/add_member", status_code=status.HTTP_201_CREATED)
def add_member(
        dialog_id: int = Body(...),
        another_user_id: int = Body(...),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    dialog_service.add_member(user, dialog_id, another_user_id)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/leave_dialog", status_code=status.HTTP_204_NO_CONTENT)
def add_member(
        dialog_id: int = Body(...),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    dialog_service.leave_dialog(user, dialog_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/remove_member", status_code=status.HTTP_204_NO_CONTENT)
def add_member(
        dialog_id: int = Body(...),
        another_user_id: int = Body(...),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    dialog_service.remove_member_from_dialog(user, dialog_id, another_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_dialog(
        dialog_id: int = Body(...),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    dialog_service.delete_dialog(user, dialog_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
