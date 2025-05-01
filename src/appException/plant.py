from utils.app_exception import AppExceptionCase


class PlantNotFound(AppExceptionCase):
    message = "Plant not found"
    status_code = 404

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)
