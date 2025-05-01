from utils.app_exception import AppExceptionCase


class NotFound(AppExceptionCase):
    def __init__(self, message: str | None = None):
        if message is None:
            message = "User not found"
        status_code = 404
        AppExceptionCase.__init__(self, status_code, message)


class UserNotFound(AppExceptionCase):
    message = "User not found"
    status_code = 404

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)


class EmailAlreadyRegistered(AppExceptionCase):
    message = "Email already registered"
    status_code = 400

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)


class NameAlreadyRegistered(AppExceptionCase):
    message = "Name already registered"
    status_code = 400

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)
