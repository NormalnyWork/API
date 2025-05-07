from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import get_settings
from database import Base, engine
from scheduler.task_scheduler import start_scheduler
from utils import include_routers
from utils.app_exception import AppExceptionCase, app_exception_handler


settings = get_settings()
app = FastAPI(title=settings.app_name)
origins = ["*"]

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(
    request: Request, e: AppExceptionCase
) -> JSONResponse:
    return await app_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"details": exc.errors(), "body": exc.body}),
    )


@app.on_event('startup')
async def startup():
    Base.metadata.create_all(bind=engine)
    include_routers(app, __file__)
    start_scheduler()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=8000)
