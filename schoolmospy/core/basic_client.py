import httpx
from typing import Any, Optional, Type
from pydantic import BaseModel
from schoolmospy.utils.exceptions import APIError, AuthError, NotFoundError, ServerError, HTTPError


class BasicClient:
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        profile_id: Optional[int] = None,
        profile_type: str = "student",
        timeout: float = 15.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.profile_id = profile_id
        self.profile_type = profile_type
        self.timeout = timeout

    @property
    def headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "dnevniklib/1.0 (Python httpx)",
            "X-mes-subsystem": "familyweb",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.profile_id:
            headers["Profile-Id"] = str(self.profile_id)
        if self.profile_type:
            headers["Profile-Type"] = self.profile_type
            headers["X-Mes-Role"]   = self.profile_type
        return headers

    async def _handle_response(self, response: httpx.Response, response_model: Optional[Type[BaseModel]] = None):
        if response.is_success:
            if response_model:
                return response_model.model_validate(response.json())
            return response.json()

        text = response.text.strip()
        status = response.status_code

        if status == 401:
            raise AuthError("Unauthorized or invalid token", status, text)
        elif status == 404:
            raise NotFoundError("Resource not found", status, text)
        elif status >= 500:
            raise ServerError("Server error", status, text)
        else:
            raise HTTPError(f"Unexpected response ({status})", status, text)

    async def get(self, endpoint: str, response_model: Optional[Type[BaseModel]] = None, **kwargs: Any):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            try:
                resp = await client.get(url, **kwargs)
            except httpx.RequestError as e:
                raise APIError(f"Request failed: {e}") from e
            return await self._handle_response(resp, response_model)

    async def post(self, endpoint: str, data: Any = None, response_model: Optional[Type[BaseModel]] = None, **kwargs: Any):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            try:
                resp = await client.post(url, json=data, **kwargs)
            except httpx.RequestError as e:
                raise APIError(f"Request failed: {e}") from e
            return await self._handle_response(resp, response_model)
