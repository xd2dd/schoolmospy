from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Pagination(BaseModel):
    page_number: int = Field(alias="pageNumber")
    page_size: int = Field(alias="pageSize")


class RewardSearchFilters(BaseModel):
    reward_types: list[str] | None = Field(alias="rewardTypes", default=None)
    statuses: list[str] | None = None
    is_empty_hidden: bool | None = Field(alias="isEmptyHidden", default=None)


class RewardSearchRequest(BaseModel):
    pagination: Pagination
    filters: RewardSearchFilters | None = None


class ProfileRewardsSorting(BaseModel):
    order_by: str = Field(alias="orderBy")
    direction: str


class ProfileRewardsRequest(BaseModel):
    pagination: Pagination
    sorting: ProfileRewardsSorting | None = None


class RewardPerson(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    is_receive_rewards_allowed: bool = Field(alias="isReceiveRewardsAllowed")


class RewardCatalogItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    status: str
    name: str
    reward_type: str = Field(alias="rewardType")
    quantity: int
    balance: int
    points: int
    image_url: str = Field(alias="imageUrl")
    animation_url: str = Field(alias="animationUrl")
    published_at: datetime = Field(alias="publishedAt")


class ProfileRewardItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    profile_reward_id: int = Field(alias="profileRewardId")
    from_user: RewardPerson = Field(alias="from")
    to_user: RewardPerson = Field(alias="to")
    sending_mode: str = Field(alias="sendingMode")
    name: str
    comment: str | None = None
    status: str
    reward_type: str = Field(alias="rewardType")
    published_at: datetime = Field(alias="publishedAt")
    purchased_at: datetime = Field(alias="purchasedAt")
    image_url: str = Field(alias="imageUrl")
    animation_url: str = Field(alias="animationUrl")


class RewardsSearchResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total_items: int = Field(alias="totalItems")
    page_number: int = Field(alias="pageNumber")
    page_size: int = Field(alias="pageSize")
    content: list[RewardCatalogItem]


class ProfileRewardsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total_items: int = Field(alias="totalItems")
    page_number: int = Field(alias="pageNumber")
    page_size: int = Field(alias="pageSize")
    content: list[ProfileRewardItem]


class RewardsSearchPayload(BaseModel):
    pagination: Pagination
    filters: dict[str, Any] | RewardSearchFilters | None = None


class ProfileRewardsPayload(BaseModel):
    pagination: Pagination
    sorting: dict[str, Any] | ProfileRewardsSorting | None = None


class GamificationProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    gamification_id: str = Field(alias="gamificationId")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    balance: int
    is_receive_rewards_allowed: bool = Field(alias="isReceiveRewardsAllowed")
    is_show_rewards_allowed: bool = Field(alias="isShowRewardsAllowed")
