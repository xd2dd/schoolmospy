from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InstantMessageContext(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    source_id: int = Field(alias="source_id")
    source_name: str = Field(alias="source_name")
    event_id: int = Field(alias="event_id")
    event_name: str = Field(alias="event_name")
    setting_group_id: int | None = Field(alias="setting_group_id", default=None)
    setting_group_name: str = Field(alias="setting_group_name")


class InstantMessageItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    description: str
    timestamp: int
    decision_required: bool
    familiarise_required: bool
    is_new: bool
    is_important: bool
    created_at: datetime
    child_id: int | None = None
    vcu_icon: str | None = None
    context: InstantMessageContext


class InstantMessagesFeed(BaseModel):
    data: list[InstantMessageItem]
