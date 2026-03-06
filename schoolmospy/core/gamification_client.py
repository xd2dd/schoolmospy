from __future__ import annotations

from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.gamification import (
    GamificationProfile,
    Pagination,
    ProfileRewardsPayload,
    ProfileRewardsResponse,
    ProfileRewardsSorting,
    RewardsSearchPayload,
    RewardsSearchResponse,
)


class GamificationClient:
    def __init__(self, client: BasicClient) -> None:
        self.client = client

    async def get_profile(self, person_id: str) -> GamificationProfile:
        """
        Get gamification profile by MES person id (contingent GUID).
        """
        params = {"personId": person_id}
        headers = {
            "x-mes-subsystem": "familymp",
            "client-type": "diary-mobile",
            "Accept-Language": "ru",
        }
        if self.client.bearer_token:
            params["apikey"] = self.client.bearer_token
            headers["auth-token"] = self.client.bearer_token

        return await self.client.get(
            "/api/gamification/v1/profiles",
            response_model=GamificationProfile,
            params=params,
            headers=headers,
        )

    async def search_rewards(
        self,
        page_number: int = 1,
        page_size: int = 20,
        reward_types: list[str] | None = None,
        statuses: list[str] | None = None,
        is_empty_hidden: bool = True,
    ) -> RewardsSearchResponse:
        """
        Search available rewards catalog.
        """
        filters: dict[str, object] = {"isEmptyHidden": is_empty_hidden}
        if reward_types is not None:
            filters["rewardTypes"] = reward_types
        if statuses is not None:
            filters["statuses"] = statuses

        payload = RewardsSearchPayload(
            pagination=Pagination(pageNumber=page_number, pageSize=page_size),
            filters=filters,
        )
        params: dict[str, str] = {}
        headers = {
            "x-mes-subsystem": "familymp",
            "client-type": "diary-mobile",
            "Accept-Language": "ru",
        }
        if self.client.bearer_token:
            params["apikey"] = self.client.bearer_token
            headers["auth-token"] = self.client.bearer_token

        return await self.client.post(
            "/api/gamification/v1/rewards/search",
            data=payload.model_dump(by_alias=True, exclude_none=True),
            response_model=RewardsSearchResponse,
            params=params,
            headers=headers,
        )

    async def get_profile_rewards(
        self,
        profile_id: int,
        from_scope: str = "ALL",
        to_scope: str = "ME",
        page_number: int = 1,
        page_size: int = 10,
        order_by: str = "purchasedAt",
        direction: str = "DESC",
    ) -> ProfileRewardsResponse:
        """
        Get rewards received/sent by profile.
        """
        payload = ProfileRewardsPayload(
            pagination=Pagination(pageNumber=page_number, pageSize=page_size),
            sorting=ProfileRewardsSorting(orderBy=order_by, direction=direction),
        )
        params = {"from": from_scope, "to": to_scope}
        headers = {
            "x-mes-subsystem": "familymp",
            "client-type": "diary-mobile",
            "Accept-Language": "ru",
        }
        if self.client.bearer_token:
            params["apikey"] = self.client.bearer_token
            headers["auth-token"] = self.client.bearer_token

        return await self.client.post(
            f"/api/gamification/v1/profiles/{profile_id}/rewards",
            data=payload.model_dump(by_alias=True, exclude_none=True),
            response_model=ProfileRewardsResponse,
            params=params,
            headers=headers,
        )
