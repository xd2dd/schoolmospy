from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class EventItem(BaseModel):
    id: int
    source_id: str
    source: str
    start_at: str
    finish_at: str
    cancelled: bool | None = None
    lesson_type: str | None = None
    course_lesson_type: Any | None = None
    lesson_form: Any | None = None
    replaced: bool | None = None
    room_name: str | None
    room_number: str | None
    subject_id: int | None = None
    subject_name: str
    link_to_join: Any | None = None
    health_status: Any
    absence_reason_id: Any
    nonattendance_reason_id: Any
    homework: Any | None = None
    marks: Any | None = None
    is_missed_lesson: bool
    esz_field_id: int | None = None
    lesson_theme: Any | None = None


class Events(BaseModel):
    total_count: int
    response: list[EventItem]
    errors: Any
