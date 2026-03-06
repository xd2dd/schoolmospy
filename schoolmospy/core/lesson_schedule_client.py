from __future__ import annotations

from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.lesson_schedule_item import LessonScheduleItem


class LessonScheduleClient:
    def __init__(self, client: BasicClient) -> None:
        self.client = client

    async def get_item(
        self,
        item_id: int,
        person_id: str,
        student_id: int | None = None,
        lesson_type: str = "PLAN",
        row_limit: int = 54,
    ) -> LessonScheduleItem:
        """
        Get lesson details by lesson schedule item id.

        Args:
            item_id (int): Lesson schedule item id.
            person_id (str): GUID of the student (contingent GUID).
            student_id (int | None): Student profile id. Defaults to current profile id.
            lesson_type (str): Lesson type param for API.
            row_limit (int): Optional response row limit.

        Returns:
            LessonScheduleItem: Typed lesson details.
        """
        resolved_student_id = student_id or self.client.profile_id
        params = {
            "student_id": resolved_student_id,
            "type": lesson_type,
            "person_id": person_id,
        }
        headers = {
            "x-mes-subsystem": "familymp",
            "client-type": "diary-mobile",
            "Accept-Language": "ru",
            "x-row-limit": str(row_limit),
        }
        if self.client.bearer_token:
            params["apikey"] = self.client.bearer_token
            headers["auth-token"] = self.client.bearer_token

        return await self.client.get(
            f"/api/family/mobile/v1/lesson_schedule_items/{item_id}",
            LessonScheduleItem,
            params=params,
            headers=headers,
        )
