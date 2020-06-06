from datetime import datetime
from praw.models import Submission as RedditSubmission
from typing import List

from clients.reddit_client import get_new_posts, make_new_reddit_client
from common.config import SUBREDDITS
from common.data_classes import RawSubmission
from common.enums import DataSource
from common.utils import clean_url, url_is_image


def run_reddit_rss_feed():
    print(f"Initializing reddit client.")
    reddit_client = make_new_reddit_client()

    print(f"Fetching posts from Reddit.")
    reddit_posts = get_new_posts(reddit_client, SUBREDDITS, 5)
    print(f"Converting Reddit posts. {reddit_posts}")
    raw_posts = convert_reddit_submission(reddit_posts)


def convert_reddit_submission(reddit_submissions: List[RedditSubmission]) -> RawSubmission:
    raw_submissions: List[RawSubmission] = []

    for reddit_submission in reddit_submissions:
        if reddit_submission.is_self or reddit_submission.stickied:
            print(f"Skipping self or stickied post with id: {reddit_submission.id}")
            continue

        clean_media_url = clean_url(reddit_submission.url)
        if url_is_image(clean_media_url):
            print(f"Skipping image post with id: {reddit_submission.id} and media url {clean_url}")
            continue
        raw_submissions.append(
            RawSubmission(
                data_source=DataSource.reddit,
                id_source=reddit_submission.id,
                submission_title=reddit_submission.title,
                submission_datetime_utc=datetime.utcfromtimestamp(int(reddit_submission.created_utc)),
                submission_community=reddit_submission.subreddit.display_name,
                submission_url=reddit_submission.permalink,
                submission_media_urls=[clean_media_url],
                submission_body="",
                id_submitter=reddit_submission.author.id,
            )
        )
    return raw_submissions
