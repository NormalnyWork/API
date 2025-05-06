from utils.app_exception import AppExceptionCase


class NotFound(AppExceptionCase):
    def __init__(self, message: str | None = None):
        if message is None:
            message = "user_not_found"
        status_code = 401
        AppExceptionCase.__init__(self, status_code, message)


class UserNotFound(AppExceptionCase):
    message = "user_not_found"
    status_code = 401

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)


class EmailAlreadyRegistered(AppExceptionCase):
    message = "email_already_registered"
    status_code = 400

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)


class NameAlreadyRegistered(AppExceptionCase):
    message = "name_already_registered"
    status_code = 400

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)
