from pydantic import BaseModel
from pydantic import Field


class ExceptionContent(BaseModel):
    type: str
    message: str


class HttpException400(BaseModel):
    status_code: int = Field(400, description="The status code", example=400)  # type: ignore
    error: ExceptionContent


class HttpException401(BaseModel):
    status_code: int = Field(401, description="The status code", example=401)  # type: ignore
    error: ExceptionContent = Field(
        ExceptionContent(
            **{"type": "HTTP_401_UNAUTHORIZED", "message": "Unauthorized"}
        ),
        description="The error content for unauthorized access",
    )
