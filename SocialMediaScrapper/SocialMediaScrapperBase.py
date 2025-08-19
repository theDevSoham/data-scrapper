from Scrapper import Scrapper, Authenticator
from typing import List, Dict, Any

# ----- Social Media Scrapper -----
class SocialMediaScrapperBase(Scrapper, Authenticator):
    
    def __init__(self):
        self._isAuthenticated: bool = False
        self._authenticate()
        
    def _authenticate(self) -> None:
        print(f"{self.__class__.__name__}: Authenticating with social media platform...")
        self._isAuthenticated = True

    def fetch_data(self) -> List[Dict[str, Any]]:
        if not self._isAuthenticated:
            self._authenticate()
        print(f"{self.__class__.__name__}: Parsing social media data...")