from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Visit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    in_time: str = Field(alias="in")
    out_time: str = Field(alias="out")
    duration: str
    person_in: Any | None = Field(alias="personIn")
    person_out: Any | None = Field(alias="personOut")
    kind_id: int = Field(alias="kindId")
    kind_name: str = Field(alias="kindName")
    is_incomplete: bool = Field(alias="isIncomplete")
    organization_id: int = Field(alias="organizationId")
    organization_name: str = Field(alias="organizationName")
    organization_short_name: str = Field(alias="organizationShortName")
    organization_address: str = Field(alias="organizationAddress")


class VisitDurationDay(BaseModel):
    date: date
    visits: list[Visit]


class VisitDurations(BaseModel):
    payload: list[VisitDurationDay]
