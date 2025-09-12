from SocialMediaScrapper import FacebookScrapper, TwitterScrapper, InstagramScrapper
from pydantic import BaseModel, model_validator
from typing import Optional, List
from utils import Parser, Normalizer, StorageGateway
from Orchestrator import Orchestrator
from Scrapper import Scrapper
from fastapi import FastAPI

app = FastAPI()

# Request body schema
class TokenRequest(BaseModel):
    instagram_token: Optional[str] = None
    facebook_token: Optional[str] = None
    twitter_token: Optional[str] = None

    @model_validator(mode="after")
    def at_least_one_token(self):
        if not any([self.instagram_token, self.facebook_token, self.twitter_token]):
            raise ValueError("At least one token must be provided")
        return self


@app.post("/scrape")
def run_scrapper(tokens: TokenRequest):
    scrappers: List[Scrapper] = []
    
    if tokens.instagram_token:
        scrappers.append(InstagramScrapper(tokens.instagram_token))
    if tokens.facebook_token:
        scrappers.append(FacebookScrapper(tokens.facebook_token))
    if tokens.twitter_token:
        scrappers.append(TwitterScrapper(tokens.twitter_token))
        
    parser = Parser()
    normalizer = Normalizer()
    storage = StorageGateway()

    orchestrator = Orchestrator.Orchestrator(
        scrappers=scrappers,
        parser=parser,
        normalizer=normalizer,
        storage_gateway=storage
    )

    try:
        orchestrator.run()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
