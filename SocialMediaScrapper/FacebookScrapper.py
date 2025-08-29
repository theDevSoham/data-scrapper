from .SocialMediaScrapperBase import SocialMediaScrapperBase
from typing import List, Dict, Any
import requests
from config.Config import APP_ID, APP_SECRET, SCOPE

# ----- Facebook Scrapper -----
class FacebookScrapper(SocialMediaScrapperBase):
    
    def __init__(self, client_token):
        super().__init__(client_token)
        self.token: str = ""
    
    def __verify_token(self, token: str) -> bool:
        print("[FacebookScrapper] Verifying token...")
        app_access_token = f"{APP_ID}|{APP_SECRET}"
        
        url = "https://graph.facebook.com/v23.0/debug_token"
        params = {
            "input_token": token,
            "access_token": app_access_token
        }
        
        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            data = res.json().get("data", {})
            
            # ✅ Step 1: Basic token validity
            if not data.get("is_valid"):
                print("[FacebookScrapper] Token is invalid ❌")
                return False
            
            # ✅ Step 2: Required scopes validation
            granted_scopes = set(data.get("scopes", [])) or set()
            required_scopes = set(scope.strip() for scope in SCOPE.split(","))

            missing_scopes = required_scopes - granted_scopes
            if missing_scopes:
                print(f"[FacebookScrapper] Missing required scopes: {missing_scopes} ❌")
                return False

            print("[FacebookScrapper] Token is valid with required scopes ✅")
            return True
        except requests.RequestException as e:
            print(f"[FacebookScrapper] Error verifying token: {e}")
            return False
        
    
    def _authenticate(self, client_token: str) -> None:
        print("[FacebookScrapper] Authenticating with Facebook API...")
        if self.__verify_token(client_token):
            self._isAuthenticated = True
            self.token = client_token
            print("[FacebookScrapper] Authentication successful.")
        else:
            raise ValueError("Invalid Facebook token")

    def fetch_data(self):
        print("[FacebookScrapper] Fetching data...")
        return [{"post": "Hello FB", "likes": 42}]