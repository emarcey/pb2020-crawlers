import logging
from datetime import datetime
from praw.models import Submission as RedditSubmission
from typing import Generator

from clients.laravel_client import bulk_upload_submissions
from clients.reddit_client import make_new_reddit_client, stream_posts
from common.config import EXPLICIT_SUBREDDITS, READER_MODE, REDDIT_LARAVEL_API_KEY, SUBREDDITS
from common.data_classes import RawSubmission
from common.enums import DataSource
from common.utils import clean_url, reddit_post_is_relevant  # , write_raw_submissions_to_csv

logger = logging.getLogger(__name__)


def run_reddit_feed():
    logger.info("Initializing reddit client.")
    reddit_client = make_new_reddit_client()

    logger.info(f"Fetching posts from Reddit.")
    reddit_posts = stream_posts(reddit_client, SUBREDDITS, READER_MODE)
    logger.info("Converting Reddit posts.")
    raw_posts = convert_reddit_submission(reddit_posts)

    for raw_post in raw_posts:
        logger.info(f"Writing reddit post with id {raw_post.id_source} to Laravel")
        bulk_upload_submissions([raw_post], REDDIT_LARAVEL_API_KEY, READER_MODE)


def convert_reddit_submission(
    reddit_submissions: Generator[RedditSubmission, None, None]
) -> Generator[RawSubmission, None, None]:
    for reddit_submission in reddit_submissions:
        if not reddit_post_is_relevant(reddit_submission, EXPLICIT_SUBREDDITS):
            continue

        yield RawSubmission(
            data_source=DataSource.reddit,
            id_source=reddit_submission.id,
            submission_title=reddit_submission.title,
            submission_datetime_utc=datetime.utcfromtimestamp(int(reddit_submission.created_utc)),
            submission_community=reddit_submission.subreddit.display_name,
            submission_url="reddit.com" + reddit_submission.permalink,
            submission_media_url=clean_url(reddit_submission.url),
            submission_body="",
            id_submitter=reddit_submission.author.id,
        )
