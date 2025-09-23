# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment

APP_ID = os.getenv("FACEBOOK_APP_ID", "")
APP_SECRET = os.getenv("FACEBOOK_APP_SECRET", "")
SCOPE = os.getenv("SCOPE", "")
PARSER_URL = os.getenv("PARSER_URL", "")
