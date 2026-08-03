class AppError(Exception):
    """Base class for domain errors. Carries the HTTP status to return."""
    status_code: int = 400

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409   # request conflicts with current state (e.g. not enough stock)