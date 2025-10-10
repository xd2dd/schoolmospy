from datetime import datetime
from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.homeworks import Homeworks


class HomeworkClient:
    def __init__(self, client: BasicClient):
        self.client = client

    async def get(self, from_date: datetime, to_date: datetime) -> Homeworks:
        return await self.client.get(
            "/api/family/web/v1/homeworks",
            Homeworks,
            params={
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
                "student_id": self.client.profile_id
            }
        )
