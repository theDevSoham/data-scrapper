from .SocialMediaScrapperBase import SocialMediaScrapperBase
import requests
from typing import List, Dict, Any

# ----- Twitter Scrapper -----
class TwitterScrapper(SocialMediaScrapperBase):
    
    def __init__(self, client_token: str):
        self.__user_id: str | None = None
        super().__init__(client_token=client_token)
    def _authenticate(self, client_token: str) -> None:
        """Authenticate client by verifying provided token."""
        print("[TwitterScrapper] Authenticating with Twitter...")
        try:
            self.__user_id = self.__verify_token(client_token)
            print(f"[TwitterScrapper] Authenticated. User ID: {self.__user_id}")
        except Exception as e:
            print(f"[TwitterScrapper] Authentication failed: {str(e)}")
            raise

    def fetch_data(self):
        """Fetch tweets for authenticated user."""
        if not self.__user_id or not self._client_token:
            raise RuntimeError("User not authenticated. Call _authenticate first.")

        url = (
            f"https://api.x.com/2/users/{self.__user_id}/tweets"
            "?max_results=100&tweet.fields=id,text,created_at,public_metrics"
            "&exclude=retweets,replies"
        )
        headers = {"Authorization": f"Bearer {self._client_token}"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            payload = response.json()

            tweets = self.__validate_tweets(payload)
            print(f"[TwitterScrapper] Retrieved {len(tweets)} tweets ✅")
            for tweet in tweets:
                print(f"  - {tweet['id']}: {tweet['text']}")

            return tweets

        except requests.RequestException as e:
            print(f"[TwitterScrapper] Error fetching tweets: {str(e)}")
            raise
        except ValueError as e:
            print(f"[TwitterScrapper] Invalid response structure: {str(e)}")
            raise
    
        # ---------- Private Helpers ----------
    def __verify_token(self, client_token: str) -> str:
        """Verify token by calling Twitter's /2/users/me endpoint."""
        url = "https://api.x.com/2/users/me"
        headers = {"Authorization": f"Bearer {client_token}"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            raise ValueError(
                f"Invalid response from Twitter API. "
                f"Status: {response.status_code}, Body: {response.text}"
            )

        return self.__get_user_id(response.json())
    
    def __get_user_id(self, payload: dict) -> str:
        """Extract user ID from API response."""
        try:
            user_id = payload["data"]["id"]
            if not user_id:
                raise KeyError("Missing user ID in response")
            return user_id
        except (KeyError, TypeError):
            raise ValueError(
                f"Could not extract user ID from response: {payload}"
            )
    def __validate_tweets(self, payload: dict) -> List[Dict[str, Any]]:
        """Validate and normalize tweets structure."""
        if "data" not in payload or not isinstance(payload["data"], list):
            raise ValueError(f"Invalid tweets response format: {payload}")

        tweets = []
        for tweet in payload["data"]:
            try:
                tweet_id = tweet["id"]
                text = tweet["text"]
                created_at = tweet["created_at"]
                metrics = tweet.get("public_metrics", {})

                tweets.append(
                    {
                        "id": tweet_id,
                        "text": text,
                        "created_at": created_at,
                        "metrics": metrics,
                    }
                )
            except KeyError as e:
                print(f"[TwitterScrapper] Skipping malformed tweet: {tweet}, error: {e}")

        return tweets