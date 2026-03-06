from __future__ import annotations

from datetime import date, datetime

from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.meals import MealComplexes


class MealsClient:
    def __init__(self, client: BasicClient) -> None:
        self.client = client

    async def get_complexes(
        self,
        on_date: date | datetime,
        person_id: str,
        row_limit: int = 27,
    ) -> MealComplexes:
        """
        Get available meal complexes for a student and date.

        Args:
            on_date (date | datetime): Date to request menu for.
            person_id (str): GUID of the student (contingent GUID).
            row_limit (int): Optional response row limit.

        Returns:
            MealComplexes: Typed list of meal complexes and their items.
        """
        date_value = on_date.date() if isinstance(on_date, datetime) else on_date
        headers: dict[str, str] = {
            "X-mes-subsystem": "familymp",
            "client-type": "diary-mobile",
            "Accept-Language": "ru",
            "x-row-limit": str(row_limit),
        }
        if self.client.bearer_token:
            headers["auth-token"] = self.client.bearer_token

        return await self.client.get(
            "/api/meals/v2/menu/complexes",
            MealComplexes,
            params={
                "onDate": date_value.isoformat(),
                "personId": person_id,
            },
            headers=headers,
        )
