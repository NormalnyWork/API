import firebase_admin
from firebase_admin import credentials, messaging

from config import get_settings

settings = get_settings()

cred = credentials.Certificate(settings.firebase_credentials_path)
firebase_admin.initialize_app(cred)

def send_fcm_notification(token: str, title: str, body: str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token,
    )
    response = messaging.send(message)
    return response #Доделать пуши
