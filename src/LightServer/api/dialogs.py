from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status, Body
from .. import models
from ..database import orm
from ..services.auth import get_current_user
from ..services.dependencies import get_user_from_id, get_dialog_from_id
from ..services.dialogs import DialogService

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
        member_ids: Optional[List[int]] = Body([]),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    return dialog_service.create(user, new_dialog, member_ids)


@router.get("/dialog_members", response_model=List[models.User])
def get_members(
        dialog: orm.Dialog = Depends(get_dialog_from_id),
        dialog_service: DialogService = Depends()
):
    return dialog_service.get_members(dialog=dialog)


@router.get("/dialog_messages", response_model=List[models.Message])
def get_messages(
        dialog: orm.Dialog = Depends(get_dialog_from_id),
        dialog_service: DialogService = Depends()
):
    return dialog_service.get_messages(dialog)


@router.post("/add_member", status_code=status.HTTP_201_CREATED)
def add_member(
        dialog: orm.Dialog = Depends(get_dialog_from_id),
        another_user: orm.User = Depends(get_user_from_id),
        dialog_service: DialogService = Depends()
):
    dialog_service.add_member(dialog, another_user)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/leave_dialog", status_code=status.HTTP_204_NO_CONTENT)
def add_member(
        dialog: orm.Dialog = Depends(get_dialog_from_id),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    dialog_service.leave_dialog(user, dialog)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/remove_member", status_code=status.HTTP_204_NO_CONTENT)
def add_member(
        dialog: orm.Dialog = Depends(get_dialog_from_id),
        another_user: orm.User = Depends(get_user_from_id),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    dialog_service.remove_member_from_dialog(user, dialog, another_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_dialog(
        dialog: orm.Dialog = Depends(get_dialog_from_id),
        user: models.User = Depends(get_current_user),
        dialog_service: DialogService = Depends()
):
    dialog_service.delete_dialog(user, dialog)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
