import firebase_admin
from firebase_admin import credentials, messaging

from config import get_settings

settings = get_settings()

cred = credentials.Certificate(settings.firebase_credentials_path)
firebase_admin.initialize_app(cred)

def send_fcm_notification(token: str, title: str, body: str):
    message = messaging.Message(
        data={
            "title": title,
            "body": body,
            "type": "care_reminder",
            "extra_info": "something_optional"
        },
        token=token,
    )
    try:
        response = messaging.send(message)
        print(f"FCM отправлено: {response}")
        return response
    except Exception as e:
        print(f"Ошибка при отправке FCM: {e}")
        return None
