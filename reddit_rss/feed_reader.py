import csv
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
    reddit_posts = get_new_posts(reddit_client, SUBREDDITS, 25)
    print(f"Converting Reddit posts. {reddit_posts}")
    raw_posts = convert_reddit_submission(reddit_posts)

    print("writing to test_file")
    write_raw_submissions_to_csv("test_file.csv", raw_posts)


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
                submission_url="reddit.com" + reddit_submission.permalink,
                submission_media_url=clean_media_url,
                submission_body="",
                id_submitter=reddit_submission.author.id,
            )
        )
    return raw_submissions


def write_raw_submissions_to_csv(target_filename: str, raw_submissions: List[RawSubmission]) -> None:
    headers = [
        "data_source",
        "id_source",
        "submission_title",
        "submission_datetime_utc",
        "submission_community",
        "submission_url",
        "submission_media_url",
        "submission_body",
        "id_submitter",
    ]

    with open(target_filename, "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(headers)

        for raw_submission in raw_submissions:
            csvwriter.writerow(
                [
                    raw_submission.data_source,
                    raw_submission.id_source,
                    raw_submission.submission_title,
                    raw_submission.submission_datetime_utc,
                    raw_submission.submission_community,
                    raw_submission.submission_url,
                    raw_submission.submission_media_url,
                    raw_submission.submission_body,
                    raw_submission.id_submitter,
                ]
            )
    pass
