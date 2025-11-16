from typing import Optional
from schoolmospy.core.basic_client import BasicClient
from schoolmospy.models.profile import Profile
from schoolmospy.models.userinfo import Userinfo
from schoolmospy.core.homeworks_client import HomeworkClient
from schoolmospy.core.marks_client import MarksClient
from schoolmospy.core.events_client import EventClient


class StudentClient(BasicClient):
    def __init__(self,
                base_url: str = "https://school.mos.ru",
                token: Optional[str] = None,
                profile_id: Optional[int] = None,
                profile_type: str = "student",
                timeout: float = 15.0):
        super().__init__(base_url, token, profile_id, profile_type, timeout)
        self.homeworks = HomeworkClient(self)
        self.marks = MarksClient(self)
        self.events = EventClient(self)


    async def get_me(self) -> Profile:
        """
        Get the current user's profile information.

        Returns:
            Profile: Profile object containing user data
        """
        return await self.get(
            "/api/family/web/v1/profile",
            Profile,
        )

    async def userinfo(self) -> Userinfo:
        """
        Get basic user information from OAuth.

        Returns:
            Userinfo: Object with basic user information
        """
        return await self.get(
            "/v1/oauth/userinfo",
            Userinfo
        )