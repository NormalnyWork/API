from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import appException
from database import get_session
from routers.auth import get_current_user, oauth2_scheme
from schema.http_exeption import HttpException400
from schema.user import UserIn, UserOut
from service.user_service import UserService

responses = {
    400: {"model": HttpException400},
}

router = APIRouter(tags=["User"], responses=responses)


@router.post("/user")
async def create_user(user: UserIn, db: Session = Depends(get_session)) -> int:
    user_id = UserService(db).create_user(user)
    return user_id


@router.get("/user", response_model=UserOut,)
async def get_user(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> UserOut:
    return UserService(db).get_user(current_user.id)

