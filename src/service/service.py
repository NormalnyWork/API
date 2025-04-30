import abc

from sqlalchemy.orm import Session


class DefaultService(abc.ABC):
    def __init__(self, session: Session) -> None:
        self.__session = session

    @property
    def session(self) -> Session:
        return self.__session
