from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Parallel(BaseModel):
    name: str
    id: int


class Organization(BaseModel):
    name: str
    global_id: int
    property_type_id: int


class Class(BaseModel):
    id: int
    uid: str
    name: str
    parallel: Parallel
    organization: Organization
    education_stage_id: int
    staff_ids: List[int]


class ServiceType(BaseModel):
    name: str
    global_id: int


class EducationItem(BaseModel):
    training_begin_at: str
    training_end_at: str
    class_: Class = Field(..., alias='class')
    service_type: ServiceType


class Picture(BaseModel):
    medium: str
    large: str


class Userinfo(BaseModel):
    email: str
    phone: str
    name: str
    gender: str
    education: List[EducationItem]
    children: List
    agents: List[str]
    mesh_id: str
    given_name: str
    family_name: str
    middle_name: str
    birth_date: str
    updated_at: str
    picture: Picture
