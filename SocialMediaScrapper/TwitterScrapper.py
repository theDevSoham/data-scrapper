from .SocialMediaScrapperBase import SocialMediaScrapperBase

# ----- Twitter Scrapper -----
class TwitterScrapper(SocialMediaScrapperBase):
    def _authenticate(self, client_token: str) -> None:
        print("[TwitterScrapper] Authenticating with Twitter...")

    def fetch_data(self):
        print("[TwitterScrapper] Fetching data...")
        return [{"post": "Hello X", "likes": 99}]