from datetime import datetime
from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.events import Events


class EventClient:
    def __init__(self, client: BasicClient):
        """
        Initialization the EventClient instance.

        Args:
            client (BasicClient): An instance of BasicClient or any compatible subclass,
                used for making API requests.
        """
        self.client = client

    async def get(self, from_date: datetime, to_date: datetime, contingent_guid: str = None) -> Events:
        """
        Method for getting events done within a certain period of time

        Args:
            from_date (datetime): The start date of the period (inclusive).
            to_date (datetime): The end date of the period (inclusive).
            contingent_guid (str): Person ID

        Returns:
            Events: A Pydantic model containing a list of events items.

        Raises:
            APIError: If the request fails or returns an unexpected response.
            AuthError: If the provided token is invalid or expired.

        Example:
            ```python
            from datetime import datetime
            from schoolmospy.clients.student_client import StudentClient

            client = StudentClient(token="YOUR_TOKEN", profile_id=17234613)
            
            me = await client.get_me()

            events = await client.events.get(
                from_date=datetime(2025, 10, 1),
                to_date=datetime(2025, 10, 24),
                contingent_guid=me.contingent_guid
            )
            print(events.response)
            ```
        """


        return await self.client.get(
            "/api/eventcalendar/v1/api/events",
            Events,
            params={
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
                "person_ids": contingent_guid,
                "expand": "marks,homework,absence_reason_id,health_status,nonattendance_reason_id",
                "source_types": "PLAN,AE,EC,EVENTS,AFISHA,ORGANIZER,OLYMPIAD,PROF"  
            }
        )
