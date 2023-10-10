from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    """Базовый класс для HTTP-исключений."""

    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL)


class NotFound(DetailedHTTPException):
    """Базовый класс для ошибок 404."""

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Not found"


class Conflict(DetailedHTTPException):
    """Базовый класс для ошибок 409."""

    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Conflict"


class BadRequest(DetailedHTTPException):
    """Базовый класс для ошибок 400."""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad request"
