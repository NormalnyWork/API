from datetime import datetime
from datetime import timedelta
from typing import Any

import appException
from database import get_session
from fastapi import HTTPException, Depends, Header, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from schema.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from schema.auth import ALGORITHM
from schema.auth import REFRESH_TOKEN_EXPIRE_MINUTES
from schema.auth import SECRET_KEY
from schema.auth import Token
from schema.error import ErrorResponse
from schema.http_exeption import HttpException400
from schema.http_exeption import HttpException401
from schema.user import UserOut
from service.user_service import UserService
from sqlalchemy.orm import Session
from starlette import status

from utils.auth import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="",
    tags=["Auth"],
    responses={401: {"model": HttpException401}, 400: {"model": HttpException400}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def create__token(data: dict[str, Any], expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_credits(user_id: int) -> tuple[str, str]:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create__token(
        data={"sub": str(user_id)}, expires_delta=access_token_expires
    )
    refresh_token_expire = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create__token(
        data={"sub": str(user_id)}, expires_delta=refresh_token_expire
    )
    return access_token, refresh_token


async def decode_token(token: str = Depends(oauth2_scheme)) -> int:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not_authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="сould_not_validate_credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if user_id := payload.get("sub"):
            user_id = int(user_id)
        else:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id


async def get_current_user(
    user_id: int = Depends(decode_token), db: Session = Depends(get_session)
) -> UserOut:
    try:
        return UserOut.model_validate(UserService(db).get_user(user_id))
    except appException.NotFound:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="сould_not_validate_credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception


@router.post("/token", response_model=Token, responses={
    406: {
        "model": ErrorResponse,
        "description": "406\n- incorrect_username_or_password"
    }})
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)
) -> Token:
    """
    ______________________________________
        вместо username вставляйте email
    ______________________________________
    """
    user = UserService(db).authenticate(form_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="incorrect_username_or_password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, refresh_token = get_user_credits(user.id)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token_in: str = Header(), db: Session = Depends(get_session)
) -> Token:
    """
    ---------------------------------------------
        refresh-token* -- refresh_token(получаем новый acces_token)
        string   обязательный параметр
    ---------------------------------------------
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token_in, SECRET_KEY, algorithms=[ALGORITHM])

        if user_id := payload.get("sub"):
            user_id = int(user_id)
        else:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    try:
        UserService(db).get_user(user_id)
    except appException.NotFound:
        raise credentials_exception

    access_token, new_refresh_token = get_user_credits(user_id)

    return Token(access_token=access_token, refresh_token=new_refresh_token)
