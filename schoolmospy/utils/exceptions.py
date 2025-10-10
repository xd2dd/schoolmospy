from typing import Optional, Any


class APIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Any] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    def __str__(self):
        return f"{self.__class__.__name__}: {self.args[0]} (status={self.status_code})"


class AuthError(APIError):
    ...

class NotFoundError(APIError):
    ...


class ServerError(APIError):
    ...


class HTTPError(APIError):
    ...
