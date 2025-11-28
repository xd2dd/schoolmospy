from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Url(BaseModel):
    url: str
    type: str


class Material(BaseModel):
    uuid: str | None
    type: str
    selected_mode: str | None
    type_name: str
    id: int | None
    urls: list[Url]
    description: Any
    content_type: Any
    title: str
    action_id: int
    action_name: str


class HomeworkItem(BaseModel):
    type: str
    description: str
    comments: list
    materials: list[Material]
    homework: str
    homework_entry_student_id: int
    attachments: list
    subject_id: int
    group_id: int
    date: str
    date_assigned_on: str
    subject_name: str
    lesson_date_time: str
    is_done: bool
    has_teacher_answer: bool
    homework_id: int
    homework_entry_id: int
    homework_created_at: str
    homework_updated_at: str
    written_answer: Any
    date_prepared_for: str


class Homeworks(BaseModel):
    payload: list[HomeworkItem]
