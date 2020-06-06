from praw import Reddit
from praw.models import Submission
import requests
from typing import List

from common.config import REDDIT_USER, REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT, REDDIT_DUMMY_REDIRECT


def make_new_reddit_client() -> Reddit:
    return Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        redirect_uri=REDDIT_DUMMY_REDIRECT,
        user_agent=REDDIT_USER_AGENT,
    )


def get_new_posts(reddit_client: Reddit, subreddits: List[str], limit: int = 100) -> List[Submission]:
    return reddit_client.subreddit("+".join(subreddits)).new(limit=limit)
