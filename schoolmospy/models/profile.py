from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class _Profile(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    birth_date: str
    sex: str
    user_id: int
    id: int
    phone: str
    email: str
    snils: str
    type: str


class School(BaseModel):
    id: int
    name: str
    short_name: str
    county: str
    principal: str
    phone: str
    global_school_id: int
    municipal_unit_name: Any


class Group(BaseModel):
    id: int
    name: str
    subject_id: int
    is_fake: bool


class Representative(BaseModel):
    person_id: str
    last_name: str
    first_name: str
    middle_name: str
    type_id: int
    type: str
    email: Optional[str]
    phone: str
    snils: str


class Section(BaseModel):
    id: int
    name: str
    subject_id: Any
    is_fake: bool


class Child(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    birth_date: str
    sex: str
    user_id: int
    id: int
    phone: str
    email: str
    snils: str
    type: Any
    school: School
    class_name: str
    class_level_id: int
    class_unit_id: int
    class_uid: str
    age: int
    groups: List[Group]
    representatives: List[Representative]
    sections: List[Section]
    sudir_account_exists: bool
    sudir_login: Any
    is_legal_representative: bool
    parallel_curriculum_id: int
    contingent_guid: str
    enrollment_date: str
    service_type_id: int
    profession_specialty_code: Any
    profession_specialty_name: Any


class Profile(BaseModel):
    profile: _Profile
    children: List[Child]
    hash: str