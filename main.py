from pydantic import BaseModel, model_validator
from typing import Optional, List
from Orchestrator import Orchestrator
from Scrapper import Scrapper
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from exceptions.exceptions import AuthenticationError, ScraperError

app = FastAPI()

# exception handlers
@app.exception_handler(AuthenticationError)
async def auth_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=401,
        content={"status": "error", "error_type": "AuthenticationError", "message": exc.message},
    )
    
@app.exception_handler(ScraperError)
async def scraper_exception_handler(request: Request, exc: ScraperError):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "error_type": "ScraperError", "message": exc.message},
    )    

# Request body schema
class TokenRequest(BaseModel):
    app_token: str

    @model_validator(mode="after")
    def at_least_one_token(self):
        if not any([self.app_token]):
            raise ValueError("At least one token must be provided")
        return self

@app.get("/health")
def health_check():
    return {"status": "success", "message": "service running"}

@app.post("/scrape")
def run_scrapper(tokens: TokenRequest):
    orchestrator = Orchestrator.Orchestrator(token=tokens.app_token)

    try:
        orchestrator.run()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
