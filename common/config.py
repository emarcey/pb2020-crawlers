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

# Reddit configs
REDDIT_USER = getenv("REDDIT_USER")
REDDIT_CLIENT_ID = getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = getenv("REDDIT_SECRET")
REDDIT_DUMMY_REDIRECT = "http://localhost:8080"
REDDIT_USER_AGENT = "script for /r/2020PoliceBrutality"
SUBREDDITS = [
    "2020PoliceBrutality",
    "BrutalityArchive",
    "news",
    "politics",
    "worldpolitics",
    "publicfreakout",
    "bad_cop_no_donut",
]
EXPLICIT_SUBREDDITS = {"2020policebrutality", "brutalityarchive"}
REDDIT_KEYWORDS = {"police", "cop", "officer"}

REDDIT_KEYWORD_REGEX = re.compile(r".*(police|cop|officer).*")

READER_MODE = getenv("READER_MODE")
if not READER_MODE:
    raise ValueError(f"READER_MODE not set.")

JOB_SLEEP_TIME_SECONDS = int(getenv("JOB_SLEEP_TIME_SECONDS", 30))


IMAGE_FORMATS = {"png", "jpg", "jpeg"}

REDDIT_LARAVEL_API_KEY = getenv("REDDIT_LARAVEL_API_KEY")
LARAVEL_HOST = getenv("LARAVEL_HOST")
LARAVEL_ENDPOINT = "api/link-submission"

TWITTER_LARAVEL_API_KEY = getenv("TWITTER_LARAVEL_API_KEY")

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

TWITTER_LAST_RUN_FILENAME = "twitter_job_last_run.json"
TWITTER_LAST_RUN_BUCKET = ""
DEFAULT_TWITTER_LAST_RUN_ID = 1270867714505158656
TWITTER_CONSUMER_KEY = getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = getenv("TWITTER_ACCESS_TOKEN_SECRET")


DATADOG_OPTIONS = {
    "statsd_socket_path": getenv(
        "DATADOG_SOCKET_PATH", "/var/run/dogstatsd/statsd.socket"
    ),
    "api_key": getenv("DATADOG_API_KEY"),
    "app_key": getenv("DATADOG_APP_KEY"),
}
