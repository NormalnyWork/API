import io
import uuid

from fastapi import File, UploadFile, APIRouter, Depends
import boto3
from botocore.client import Config

from config import get_settings
from routers.auth import get_current_user
from schema.user import UserOut

settings = get_settings()

router = APIRouter(prefix="/file", tags=["File"])

s3 = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    config=Config(signature_version='s3v4'),
    region_name='ru-central1'
)

BUCKET_NAME = 'blum-bucket'


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user: UserOut = Depends(get_current_user)):
    file_data = await file.read()

    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"

    s3.upload_fileobj(
        Fileobj=io.BytesIO(file_data),
        Bucket=BUCKET_NAME,
        Key=unique_filename,
        ExtraArgs={"ACL": "public-read"}
    )

    file_url = f"https://storage.yandexcloud.net/{BUCKET_NAME}/{unique_filename}"

    return {"filename": unique_filename, "file_url": file_url}
