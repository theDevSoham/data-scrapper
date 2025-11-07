from Scrapper import Scrapper
from typing import List
from config.Config import SOCIAL_AUTHENTICATOR_URL
from SocialMediaScrapper import FacebookScrapper, TwitterScrapper, InstagramScrapper
import requests

# ---------- Orchestrator ----------
class Orchestrator:
    def __init__(self, token: str):
        self.scrappers: List[Scrapper] = []
        self._user_details = self._get_user_details(app_token=token)
        self._init_scrappers(self._user_details)

    def run(self):
        print("[Orchestrator] Starting scraping workflow...")
        for scrapper in self.scrappers:
            print(f"[Orchestrator] Using {scrapper.__class__.__name__}...")
            raw_data = scrapper.fetch_data()
            print(f"[Orchestrator] Received raw data of length {len(raw_data)}")
            scrapper.parse_data(raw_data)
        print("[Orchestrator] Workflow complete!")

    def _get_user_details(self, app_token: str):
        """
        Fetches user details from the social authenticator service using the given app token.
        Returns normalized user details with only the relevant fields.
        """
        try:
            url = f"{SOCIAL_AUTHENTICATOR_URL.rstrip('/')}/get_user"
            headers = {"Authorization": f"Bearer {app_token}"}

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            claims = data.get("claims", {})

            normalized_details = {
                "provider": claims.get("provider"),
                "social_id": claims.get("social_id"),
                "social_token": claims.get("social_token"),
                "name": claims.get("name"),
                "email": claims.get("email"),
            }

            print(f"[Orchestrator] Retrieved user details for provider: {normalized_details['provider']}")
            return normalized_details

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch user details: {e}")
        except Exception as e:
            raise Exception(f"Error while processing user details: {e}")
        
    def _init_scrappers(self, user_details):
        provider = user_details["provider"]
        social_id = user_details["social_id"]
        social_token = user_details["social_token"]
        name = user_details["name"]
        email = user_details["email"]

        match(provider):
            case "facebook":
                self.scrappers.append(FacebookScrapper(client_token=social_token, social_id=social_id, name=name, email=email))
            case "twitter":
                self.scrappers.append(TwitterScrapper(client_token=social_token, social_id=social_id, name=name, email=email))
            case "instagram":
                self.scrappers.append(InstagramScrapper(client_token=social_token, social_id=social_id, name=name, email=email))
            case _:
                raise Exception(f"Error: Provider not found")
