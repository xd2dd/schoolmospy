from __future__ import annotations

from datetime import date, datetime

from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.visit_durations import VisitDurations


class EntrancesClient:
    def __init__(self, client: BasicClient) -> None:
        self.client = client

    async def get_visit_durations(
        self,
        person_id: str,
        from_date: date | datetime,
        to_date: date | datetime,
        role_id: str = "7:1",
    ) -> VisitDurations:
        """
        Get school visit durations for the selected period.

        Args:
            person_id (str): GUID of the student (contingent GUID).
            from_date (date | datetime): Start date (inclusive).
            to_date (date | datetime): End date (inclusive).
            role_id (str): MES role id sent in request headers.

        Returns:
            VisitDurations: Typed list of visits grouped by date.
        """
        from_value = from_date.date() if isinstance(from_date, datetime) else from_date
        to_value = to_date.date() if isinstance(to_date, datetime) else to_date
        params = {
            "personId": person_id,
            "from": from_value.isoformat(),
            "to": to_value.isoformat(),
        }
        headers = {
            "x-mes-subsystem": "familymp",
            "client-type": "diary-mobile",
            "Accept-Language": "ru",
            "x-mes-roleid": role_id,
        }
        if self.client.bearer_token:
            params["apikey"] = self.client.bearer_token
            headers["auth-token"] = self.client.bearer_token

        return await self.client.get(
            "/api/pass/entrances/v1/visit_durations",
            VisitDurations,
            params=params,
            headers=headers,
        )
