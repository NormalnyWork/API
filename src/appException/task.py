from utils.app_exception import AppExceptionCase


class TaskNotFound(AppExceptionCase):
    message = "task_not_found"
    status_code = 404

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)