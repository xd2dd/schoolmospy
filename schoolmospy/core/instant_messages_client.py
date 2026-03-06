from __future__ import annotations

from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.instant_messages import InstantMessagesFeed


class InstantMessagesClient:
    def __init__(self, client: BasicClient) -> None:
        self.client = client

    async def get_feed(
        self,
        page: int = 1,
        npp: int = 10,
        role_id: str = "7:1",
    ) -> InstantMessagesFeed:
        """
        Get notifications feed.

        Args:
            page (int): Feed page number.
            npp (int): Number of items per page.
            role_id (str): MES role id sent in request headers.

        Returns:
            InstantMessagesFeed: Typed notifications feed.
        """
        params = {
            "page": page,
            "npp": npp,
        }
        headers = {
            "x-mes-subsystem": "familymp",
            "client-type": "diary-mobile",
            "Accept-Language": "ru",
            "x-mes-roleid": role_id,
        }
        if self.client.bearer_token:
            params["apikey"] = self.client.bearer_token
            headers["auth-token"] = self.client.bearer_token

        return await self.client.get(
            "/api/instantmessages/v1/feed",
            InstantMessagesFeed,
            params=params,
            headers=headers,
        )
