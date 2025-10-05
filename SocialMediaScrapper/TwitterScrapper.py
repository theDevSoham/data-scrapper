from .SocialMediaScrapperBase import SocialMediaScrapperBase
import requests
from typing import List, Dict, Any, Optional
from config.Config import PARSER_URL
from exceptions.exceptions import AuthenticationError, ScraperError

# ----- Twitter Scrapper -----
class TwitterScrapper(SocialMediaScrapperBase):
    
    def _authenticate(self, client_token: str) -> None:
        """Authenticate client by verifying provided token."""
        print("[TwitterScrapper] Authenticating with Twitter...")
        try:
            self._user_id = self.__verify_token(client_token)
            print(f"[TwitterScrapper] Authenticated. User ID: {self._user_id}")
        except Exception as e:
            print(f"[TwitterScrapper] Authentication failed: {str(e)}")
            raise AuthenticationError(f"Twitter authentication failed: {str(e)}")

    def fetch_data(self):
        """Fetch tweets for authenticated user."""
        if not self._user_id or not self._client_token:
            raise ScraperError("Not authenticated. Please authenticate first.")

        url = (
            f"https://api.x.com/2/users/{self._user_id}/tweets"
            "?max_results=100&tweet.fields=id,text,created_at,public_metrics"
            "&exclude=retweets,replies"
        )
        headers = {"Authorization": f"Bearer {self._client_token}"}

        try:
            # response = requests.get(url, headers=headers, timeout=10)
            # response.raise_for_status()
            twitter_sample = {
                "data": [ 
                    {
                        "text": "🦅 https://t.co/FnR3dqIWtL", 
                        "created_at": "2024-10-16T12:58:35.000Z", 
                        "id": "1846536216969089037", 
                        "public_metrics": { 
                            "retweet_count": 0, 
                            "reply_count": 0, 
                            "like_count": 0, 
                            "quote_count": 0, 
                            "bookmark_count": 0, 
                            "impression_count": 12 
                        }, 
                        "edit_history_tweet_ids": [ "1846536216969089037" ] 
                    } 
                ],
                "meta": { 
                    "result_count": 1, 
                    "newest_id": "1846536216969089037", 
                    "oldest_id": "1846536216969089037" 
                } 
            }
            # payload = response.json()
            payload = twitter_sample

            tweets = self.__validate_tweets(payload)
            print(f"[TwitterScrapper] Retrieved {len(tweets)} tweets ✅")
            for tweet in tweets:
                print(f"  - {tweet['id']}: {tweet['text']}")

            return tweets

        except requests.RequestException as e:
            print(f"[TwitterScrapper] Error fetching tweets: {str(e)}")
            raise ScraperError(f"Twitter API request failed: {str(e)}")
        except ValueError as e:
            print(f"[TwitterScrapper] Invalid response structure: {str(e)}")
            raise ScraperError(f"Twitter data parsing failed: {str(e)}")
    
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
    
    def parse_data(self, posts: List[Dict[str, Any]], meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sends a batch of Twitter posts to the parse-and-push endpoint.

        Args:
            posts: List of raw Twitter post dicts
            meta: Optional metadata dict (will be auto-generated if not provided)

        Returns:
            Dict containing the API response or an error message.
        """

        if not isinstance(posts, list):
            return {"error": "posts must be a list"}

        def _to_int(v):
            try:
                return int(v)
            except Exception:
                return 0

        normalized_posts: List[Dict[str, Any]] = []
        for p in posts:
            pub = p.get("public_metrics") or p.get("metrics") or {}
            edit_ids = p.get("edit_history_tweet_ids") or []

            normalized = {
                "id": str(p.get("id", "")),
                "text": p.get("text", "") or "",
                "created_at": p.get("created_at", "") or p.get("created_time", ""),
                "public_metrics": {
                    "retweet_count": _to_int(pub.get("retweet_count", 0)),
                    "reply_count": _to_int(pub.get("reply_count", 0)),
                    "like_count": _to_int(pub.get("like_count", 0)),
                    "quote_count": _to_int(pub.get("quote_count", 0)),
                    "bookmark_count": _to_int(pub.get("bookmark_count", 0)),
                    "impression_count": _to_int(pub.get("impression_count", 0)),
                },
                "edit_history_tweet_ids": [str(x) for x in edit_ids] if edit_ids else [str(p.get("id", ""))],
            }

            normalized_posts.append(normalized)

        # Auto-generate meta if not provided
        if meta is None:
            result_count = len(normalized_posts)
            newest_id = normalized_posts[0]["id"] if normalized_posts else ""
            oldest_id = normalized_posts[-1]["id"] if normalized_posts else ""
            meta = {
                "result_count": result_count,
                "newest_id": newest_id,
                "oldest_id": oldest_id
            }
        else:
            meta.setdefault("result_count", len(normalized_posts))
            if "newest_id" not in meta and normalized_posts:
                meta["newest_id"] = normalized_posts[0]["id"]
            if "oldest_id" not in meta and normalized_posts:
                meta["oldest_id"] = normalized_posts[-1]["id"]

        payload = {"platform": "twitter", "payload": {"data": normalized_posts, "meta": meta}}

        try:
            resp = requests.post(PARSER_URL, json=payload, timeout=60)
            resp.raise_for_status()
            try:
                return resp.json()
            except ValueError:
                return {
                    "error": "Parser returned non-JSON response",
                    "status_code": resp.status_code,
                    "body": resp.text
                }
        except requests.RequestException as exc:
            raise RuntimeError(f'{str(exc)}')

    
    # def parse_data(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    #     """
    #     Sends a batch of Twitter posts to the parse-and-push endpoint.
    #     """
    #     print("[TwitterScrapper] Parsing data...")

    #     normalized_posts = []
    #     for post in posts:
    #         normalized_post = {
    #             "id": post.get("id", ""),
    #             "created_time": post.get("created_at", ""),
    #             "text": post.get("text", ""),
    #             "metrics": {
    #                 "retweet_count": post.get("metrics", {}).get("retweet_count", 0),
    #                 "reply_count": post.get("metrics", {}).get("reply_count", 0),
    #                 "like_count": post.get("metrics", {}).get("like_count", 0),
    #                 "quote_count": post.get("metrics", {}).get("quote_count", 0),
    #                 "bookmark_count": post.get("metrics", {}).get("bookmark_count", 0),
    #                 "impression_count": post.get("metrics", {}).get("impression_count", 0),
    #             },
    #             "attachments": {"data": post.get("attachments", []) if post.get("attachments") else []},
    #         }
    #         normalized_posts.append(normalized_post)

    #     payload = {"platform": "twitter", "payload": {"data": normalized_posts}}

    #     try:
    #         response = requests.post(PARSER_URL, json=payload, timeout=60)
    #         response.raise_for_status()  # Raise exception for HTTP errors
    #         result = response.json()
    #         print(f"[TwitterScrapper] Result: {result}")
    #         return result

    #     except requests.RequestException as e:
    #         print(f"[TwitterScrapper] Error sending data: {e}")
    #         raise RuntimeError(f"Error sending data: {e}")