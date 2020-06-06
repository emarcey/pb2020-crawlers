from dotenv import load_dotenv
from os import getenv
from pathlib import Path  # python3 only
import re


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Mongo creds
MONGO_HOSTNAME = getenv("MONGO_HOSTNAME")
MONGO_USERNAME = getenv("MONGO_USERNAME")
MONGO_PASSWORD = getenv("MONGO_PASSWORD")
MONGO_DBNAME = getenv("MONGO_DBNAME")

# Reddit API creds
REDDIT_USER = getenv("REDDIT_USER")
REDDIT_CLIENT_ID = getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = getenv("REDDIT_SECRET")
REDDIT_DUMMY_REDIRECT = "http://localhost:8080"
REDDIT_USER_AGENT = "script for /r/2020PoliceBrutality"
SUBREDDITS = ["2020PoliceBrutality", "BrutalityArchive"]
REDDIT_SIZE = 5


READER_MODE = getenv("READER_MODE")
if not READER_MODE:
    raise ValueError(f"READER_MODE not set.")

JOB_SLEEP_TIME_SECONDS = int(getenv("JOB_SLEEP_TIME_SECONDS"))
if not JOB_SLEEP_TIME_SECONDS:
    JOB_SLEEP_TIME_SECONDS = 30


IMAGE_FORMATS = {"png", "jpg", "jpeg"}
