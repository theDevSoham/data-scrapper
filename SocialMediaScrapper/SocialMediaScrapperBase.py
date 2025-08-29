from Scrapper import Scrapper, Authenticator
from typing import List, Dict, Any

# ----- Social Media Scrapper -----
class SocialMediaScrapperBase(Scrapper, Authenticator):
    def __init__(self, client_token: str):
        self._isAuthenticated: bool = False
        self._client_token = client_token
        self._authenticate(client_token=client_token)
        
    def _authenticate(self, client_token: str) -> None:
        print(f"{self.__class__.__name__}: Authenticating with social media platform using token {client_token}...")
        self._isAuthenticated = True

    def fetch_data(self) -> List[Dict[str, Any]]:
        if not self._isAuthenticated:
            self._authenticate()
        print(f"{self.__class__.__name__}: Parsing social media data...")