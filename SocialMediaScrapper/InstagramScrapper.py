from .SocialMediaScrapperBase import SocialMediaScrapperBase
from typing import List, Dict, Any

# ---------- Instagram Scrapper ----------
class InstagramScrapper(SocialMediaScrapperBase):
    def _authenticate(self, client_token: str) -> None:
        print("[InstagramScrapper] Authenticating with Instagram API...")

    def fetch_data(self) -> List[Dict[str, Any]]:
        print("[InstagramScrapper] Fetching data...")
        return [{"post": "Hello IG", "likes": 99}]