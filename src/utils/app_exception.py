from starlette.requests import Request
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, message: str | None = None) -> None:
        self.message = message
        self.status_code = status_code

    @property
    def exception_case(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - message={self.message}>"
        )

    @property
    def content(self) -> dict[str, str | int]:
        return {
            "status_code": self.status_code,
            "message": self.message or "",
        }


async def app_exception_handler(
    request: Request, exc: AppExceptionCase
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )
