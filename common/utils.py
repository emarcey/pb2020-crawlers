import logging
import csv

from praw.models import Submission
from typing import Set, List

from common.data_classes import RawSubmission
from common.config import IMAGE_FORMATS, REDDIT_KEYWORD_REGEX

logger = logging.getLogger(__name__)


def clean_url(url: str) -> str:
    if "twitter" not in url:
        return url

    split_url = url.split("?")
    if len(split_url) == 0:
        return url

    return split_url[0]


def url_is_image(url: str) -> bool:
    split_url = url.split(".")
    if len(split_url) == 0:
        return False

    if split_url[-1] in IMAGE_FORMATS:
        return True

    return False


# @EM should this really be in common.utils?
def reddit_post_is_relevant(reddit_submission: Submission, explicit_subreddits: Set[str]) -> bool:
    if reddit_submission.is_self or reddit_submission.stickied:
        logger.info(f"Skipping self or stickied post with id: {reddit_submission.id}")
        return False

    if not hasattr(reddit_submission, "media") or reddit_submission.media is None:
        logger.info(f"Skipping post without media with id: {reddit_submission.id}")
        return False

    clean_media_url = clean_url(reddit_submission.url)
    if url_is_image(clean_media_url):
        logger.info(f"Skipping image post with id: {reddit_submission.id} and media url {clean_url}")
        return False

    if reddit_submission.subreddit.display_name.lower() in explicit_subreddits:
        return True

    if REDDIT_KEYWORD_REGEX.match(reddit_submission.title.lower()) is not None:
        return True

    return False


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
                    raw_submission.data_source.value,
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
