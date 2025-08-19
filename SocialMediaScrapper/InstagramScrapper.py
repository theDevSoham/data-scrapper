from .SocialMediaScrapperBase import SocialMediaScrapperBase
from typing import List, Dict, Any

# ---------- Instagram Scrapper ----------
class InstagramScrapper(SocialMediaScrapperBase):
    def _authenticate(self) -> None:
        print("[InstagramScrapper] Authenticating with Instagram API...")

    def fetch_data(self) -> List[Dict[str, Any]]:
        if not self._isAuthenticated:
            self._authenticate()
        print("[InstagramScrapper] Fetching data...")
        return [{"post": "Hello IG", "likes": 99}]