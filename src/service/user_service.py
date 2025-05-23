

import appException
from config import get_settings
from database.user import User
from schema.auth import pwd_context
from schema.user import UserIn, UserBase
from service.service import DefaultService
from utils.auth import OAuth2PasswordRequestForm

settings = get_settings()


class UserService(DefaultService):
    def create_user(self, user: UserIn) -> int:
        if self.session.query(User).filter_by(email=user.email).first():
            raise appException.user.EmailAlreadyRegistered()

        db_user = User(name=user.name,
                       email=user.email,
                       password=user.password)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user.id

    def get_user(self, user_id: int) -> User:
        user = self.session.query(User).filter_by(id=user_id).one_or_none()
        if user is None:
            raise appException.user.UserNotFound()
        return user

    def delete_user(self, user_id: int) -> None:
        user = self.session.query(User).filter_by(id=user_id).one_or_none()
        if user is None:
            raise appException.user.NotFound()
        self.session.delete(user)
        self.session.commit()

    def update(self, user: UserBase, user_id: int) -> None:
        if self.session.query(User).filter_by(email=user.email).first():
            raise appException.user.EmailAlreadyRegistered()
        if self.session.query(User).filter_by(name=user.name).first():
            raise appException.user.NameAlreadyRegistered()
        dump_data = user.model_dump(mode="json", exclude_none=True)
        self.session.query(User).filter_by(id=user_id).update(values=dump_data)  # type: ignore
        self.session.commit()

    def authenticate(self, user: OAuth2PasswordRequestForm) -> User | None:
        user_in_db = self.session.query(User).filter_by(email=user.email).one_or_none()
        if user_in_db is None:
            return None

        verify = self.verify_password(user.password, user_in_db.password)
        if not verify:
            return None
        return user_in_db

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

