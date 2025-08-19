from .SocialMediaScrapperBase import SocialMediaScrapperBase

# ----- Twitter Scrapper -----
class TwitterScrapper(SocialMediaScrapperBase):
    def _authenticate(self) -> None:
        print("[TwitterScrapper] Authenticating with Twitter...")

    def fetch_data(self):
        if not self._isAuthenticated:
            self._authenticate()
        print("[TwitterScrapper] Fetching data...")
        return [{"post": "Hello X", "likes": 99}]