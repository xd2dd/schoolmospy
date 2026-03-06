from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LessonTeacher(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    last_name: str
    first_name: str
    middle_name: str | None = None
    birth_date: str | None = None
    sex: str | None = None
    user_id: int | None = Field(alias="user_id", default=None)


class LessonMaterialUrl(BaseModel):
    url: str
    type: str


class LessonMaterial(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: str | None = None
    type: str | None = None
    selected_mode: str | None = None
    type_name: str
    id: int | None = None
    urls: list[LessonMaterialUrl]
    description: str | None = None
    content_type: str | None = None
    title: str | None = None
    action_id: int = Field(alias="action_id")
    action_name: str = Field(alias="action_name")


class HomeworkToGive(BaseModel):
    id: int


class LessonHomework(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    homework: str
    homework_entry_student_id: int
    homework_id: int
    homework_entry_id: int
    attachments: list[Any]
    homework_created_at: datetime
    homework_updated_at: datetime
    is_done: bool
    additional_materials: list[LessonMaterial]
    written_answer: Any | None = None
    date_assigned_on: datetime
    date_prepared_for: datetime
    is_smart: bool
    auto_generated: bool


class LessonThemeFrame(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int | None = None
    title: str | None = None
    theme_integration_id: int | None = Field(alias="themeIntegrationId", default=None)
    average_mark: float | None = None
    theme_frames: list[LessonThemeFrame] = Field(default_factory=list)
    oge_task_name: str | list[str] | None = None
    ege_task_name: str | list[str] | None = None


class LessonDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    content: list[Any]
    theme: LessonThemeFrame | None = None
    lesson_id: int | None = Field(alias="lessonId", default=None)
    lesson_topic: str | None = None
    additional_materials: list[LessonMaterial]


class LessonScheduleItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    group_id: int
    subject_id: int
    plan_id: int
    date: date
    begin_time: str
    begin_utc: int
    end_time: str
    end_utc: int
    subject_name: str
    teacher: LessonTeacher
    course_lesson_type: Any | None = None
    room_number: str | None = None
    room_name: str | None = None
    building_name: str | None = None
    marks: list[Any]
    created_date_time: str | None = None
    is_missed_lesson: bool
    lesson_type: str
    field_name: str | None = None
    comment: str | None = None
    lesson_homeworks: list[LessonHomework]
    homework_to_give: list[HomeworkToGive]
    details: LessonDetails
    esz_field_id: int | None = None
    teacher_comments: list[Any]
    lesson_type_nsi: Any | None = None
    remote_lesson: Any | None = None
    control: Any | None = None
    evaluation: Any | None = None
    lesson_education_type: str | None = None
    disease_status_type: Any | None = None
    theme_mastery: Any | None = None
    is_virtual: bool
    homework_presence_status_id: int | None = None
    kr_attachments: list[Any]
