from typing import Any


class APIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.args[0]} ({self.status_code}) {self.response}"


class AuthError(APIError): ...


class NotFoundError(APIError): ...


class ServerError(APIError): ...


class HTTPError(APIError): ...
