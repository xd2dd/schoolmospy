from datetime import datetime
from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.marks import Marks


class MarksClient:
    def __init__(self, client: BasicClient):
        self.client = client

    async def get(self, from_date: datetime, to_date: datetime) -> Marks:
        """
        Method for getting marks done within a certain period of time

        Args:
            from_date (datetime): The start date of the period (inclusive).
            to_date (datetime): The end date of the period (inclusive).

        Returns:
            Marks: A Pydantic model containing a list of marks items.

        Raises:
            APIError: If the request fails or returns an unexpected response.
            AuthError: If the provided token is invalid or expired.

        Example:
            ```python
            from datetime import datetime
            from schoolmospy.clients.student_client import StudentClient

            client = StudentClient(token="YOUR_TOKEN", profile_id=17234613)
            marks = await client.marks.get(
                from_date=datetime(2025, 10, 1),
                to_date=datetime(2025, 10, 24)
            )
            print(marks.payload)
            ```
        """
        return await self.client.get(
            "/api/family/web/v1/marks",
            Marks,
            params={
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
                "student_id": self.client.profile_id
            }
        )
