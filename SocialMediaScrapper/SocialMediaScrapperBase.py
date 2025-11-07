from Scrapper import Scrapper
from typing import List, Dict, Any

# ----- Social Media Scrapper -----
class SocialMediaScrapperBase(Scrapper):
    def __init__(self, app_token, client_token: str, social_id: str, name: str, email: str):
        self._client_token = client_token
        self._user_id = social_id
        self._name = name
        self._email = email
        self._app_token = app_token

    def fetch_data(self) -> List[Dict[str, Any]]:
        print(f"{self.__class__.__name__}: Parsing social media data...")
        
    def parse_data(self, posts: List) -> None:
        print(f"{self.__class__.__name__}: Parsing social media data...")