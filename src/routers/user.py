from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from const import defaultNULL
from database import get_session, User
from routers.auth import get_current_user
from schema.error import ErrorResponse
from schema.http_exeption import HttpException400, HttpException401
from schema.user import UserIn, UserOut, UserBase
from service.user_service import UserService

responses = {
    400: {"model": HttpException400}, 401: {"model": HttpException401}
}

router = APIRouter(tags=["User"], responses=responses)


@router.post("/user", responses={
    400: {
        "model": ErrorResponse,
        "description": "400 Bad Request:\n- email_already_registered\n- name_already_registered"
    }
})
async def create_user(user: UserIn, db: Session = Depends(get_session)) -> int:
    user_id = UserService(db).create_user(user)
    return user_id


@router.get("/user", response_model=UserOut, responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- user_not_found"},
})
async def get_user(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> User:
    return UserService(db).get_user(current_user.id)


@router.delete("/user", responses={200: defaultNULL})
async def delete_user(current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_session)) -> None:
    UserService(db).delete_user(current_user.id)


@router.patch("/user", responses={200: defaultNULL})
async def update_user(
    user: UserBase,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> None:
    UserService(db).update(user, current_user.id)
    return None