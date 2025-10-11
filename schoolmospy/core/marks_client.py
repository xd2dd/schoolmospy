from datetime import datetime
from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.marks import Marks


class MarksClient:
    def __init__(self, client: BasicClient):
        self.client = client

    async def get(self, from_date: datetime, to_date: datetime) -> Marks:
        return await self.client.get(
            "/api/family/web/v1/marks",
            Marks,
            params={
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
                "student_id": self.client.profile_id
            }
        )
