from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class EventItem(BaseModel):
    id: int
    source_id: str
    source: str
    start_at: str
    finish_at: str
    cancelled: Optional[bool] = None
    lesson_type: Optional[str] = None
    course_lesson_type: Optional[Any] = None
    lesson_form: Optional[Any] = None
    replaced: Optional[bool] = None
    room_name: Optional[str]
    room_number: Optional[str]
    subject_id: Optional[int] = None
    subject_name: str
    link_to_join: Optional[Any] = None
    health_status: Any
    absence_reason_id: Any
    nonattendance_reason_id: Any
    homework: Optional[Any] = None
    marks: Optional[Any] = None
    is_missed_lesson: bool
    esz_field_id: Optional[int] = None
    lesson_theme: Optional[Any] = None


class Events(BaseModel):
    total_count: int
    response: List[EventItem]
    errors: Any