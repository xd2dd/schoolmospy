from datetime import datetime
from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.homeworks import Homeworks


class HomeworkClient:
    def __init__(self, client: BasicClient):
        """
        Initialization the HomeworkClient instance.

        Args:
            client (BasicClient): An instance of BasicClient or any compatible subclass,
                used for making API requests.
        """
        self.client = client

    async def get(self, from_date: datetime, to_date: datetime) -> Homeworks:
        """
        Method for getting homework done within a certain period of time

        Args:
            from_date (datetime): The start date of the period (inclusive).
            to_date (datetime): The end date of the period (inclusive).

        Returns:
            Homeworks: A Pydantic model containing a list of homework items.

        Raises:
            APIError: If the request fails or returns an unexpected response.
            AuthError: If the provided token is invalid or expired.

        Example:
            ```python
            from datetime import datetime
            from schoolmospy.clients.student_client import StudentClient

            client = StudentClient(token="YOUR_TOKEN", profile_id=17234613)
            homeworks = await client.homework.get(
                from_date=datetime(2025, 10, 1),
                to_date=datetime(2025, 10, 24)
            )
            print(homeworks.payload)
            ```
        """


        return await self.client.get(
            "/api/family/web/v1/homeworks",
            Homeworks,
            params={
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
                "student_id": self.client.profile_id
            }
        )
