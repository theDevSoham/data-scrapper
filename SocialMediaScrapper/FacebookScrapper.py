from .SocialMediaScrapperBase import SocialMediaScrapperBase
from typing import List, Dict, Any
import requests
from config.Config import PARSER_URL
from exceptions.exceptions import ScraperError

# ----- Facebook Scrapper -----
class FacebookScrapper(SocialMediaScrapperBase):
    def fetch_data(self):
        """Fetch latest 150 posts from Facebook Graph API for the authenticated user."""
        if not self._user_id:
            raise ScraperError("Not authenticated. Please authenticate first.")

        print("[FacebookScrapper] Fetching posts data from Facebook...")

        url = f"https://graph.facebook.com/v23.0/{self._user_id}/posts"
        params = {
            "access_token": self._client_token,
            "limit": 150,  # fetch 150 posts at once
            "fields": (
                "id,message,created_time,permalink_url,"
                "attachments{media_type,media,url},"
                "reactions.summary(true),"
                "comments.summary(true){id,from,message,created_time,like_count,reactions.summary(true)}"
            )
        }

        try:
            res = requests.get(url, params=params, timeout=180)
            res.raise_for_status()
            data = res.json()

            posts = data.get("data", [])
            if not isinstance(posts, list):
                raise ValueError("Unexpected response format: 'data' is not a list")

            print(f"[FacebookScrapper] Retrieved {len(posts)} posts ✅")

            # 🔍 Print raw posts data for debugging
            for idx, post in enumerate(posts[:5], start=1):  # show only first 5 for sanity
                print(f"\n[Post {idx}] {post}")

            return posts

        except requests.RequestException as e:
            print(f"[FacebookScrapper] Request error while fetching posts: {e}")
            raise ScraperError(f"Facebook API request failed: {str(e)}")
        except ValueError as ve:
            print(f"[FacebookScrapper] Data validation error: {ve}")
            raise ScraperError(f"Facebook API request failed: {str(ve)}")
        
    def parse_data(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Sends a batch of posts to the parse-and-push endpoint.
        """
        print("[FacebookScrapper] Parsing data...")

        normalized_posts = []
        for post in posts:
            normalized_post = {
                "id": post.get("id", ""),
                "created_time": post.get("created_time", ""),
                "permalink_url": post.get("permalink_url", ""),
                "attachments": {"data": post.get("attachments", {}).get("data", []) if post.get("attachments") else []},
                "reactions": {
                    "data": post.get("reactions", {}).get("data", []),
                    "summary": post.get("reactions", {}).get(
                        "summary", {"total_count": 0, "viewer_reaction": "NONE"}
                    ),
                },
                "comments": {
                    "data": post.get("comments", {}).get("data", []),
                    "summary": post.get("comments", {}).get(
                        "summary", {"order": "chronological", "total_count": 0, "can_comment": True}
                    ),
                },
            }
            normalized_posts.append(normalized_post)

        payload = {"platform": "facebook", "payload": {"data": normalized_posts}, "token": self._client_token}

        try:
            response = requests.post(PARSER_URL, json=payload, timeout=240)
            response.raise_for_status()  # Raise exception for HTTP errors
            result = response.json()
            print(f"[FacebookScrapper] Result: {result}")
            return result

        except requests.RequestException as e:
            print(f"[FacebookScrapper] Error sending data: {e}")
            return {"error": str(e)}