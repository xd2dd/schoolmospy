from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel


class Grade(BaseModel):
    origin: str
    five: float
    ten: float
    hundred: float


class Value(BaseModel):
    name: str
    nmax: float
    grade: Grade
    grade_system_id: int
    grade_system_type: str


class MarkItem(BaseModel):
    id: int
    value: str
    values: List[Value]
    comment: str
    weight: int
    point_date: Any
    control_form_name: str
    comment_exists: bool
    created_at: str
    updated_at: str
    criteria: Any
    date: str
    subject_name: str
    subject_id: int
    has_files: bool
    is_point: bool
    is_exam: bool
    original_grade_system_type: str


class Marks(BaseModel):
    payload: List[MarkItem]