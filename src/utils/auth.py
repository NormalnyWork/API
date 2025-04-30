from typing import Annotated

from fastapi.param_functions import Form
from pydantic import EmailStr
from typing_extensions import Doc


class OAuth2PasswordRequestForm:
    def __init__(
        self,
        *,
        username: Annotated[
            EmailStr,
            Form(),
            Doc(
                """
                `email` string. The OAuth2 spec requires the exact field name
                `email`.
                """
            ),
        ],
        password: Annotated[
            str,
            Form(),
            Doc(
                """
                `password` string. The OAuth2 spec requires the exact field name
                `password".
                """
            ),
        ],
    ):
        self.email = username
        self.password = password
