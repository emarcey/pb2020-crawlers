import logging
import time

from common.config import JOB_SLEEP_TIME_SECONDS, READER_MODE
from reddit.feed_reader import run_reddit_rss_feed
from twitter.searcher import run_twitter_searches

logging.basicConfig()
logging.root.setLevel(logging.INFO)


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        while True:
            logger.info(f"Job Starting.")
            if READER_MODE == "reddit":
                run_reddit_rss_feed()
            elif READER_MODE == "twitter":
                run_twitter_searches()
                exit(0)
            else:
                raise ValueError(f"READER_MODE {READER_MODE} not supported")
            logger.info(f"Job complete. Sleeping for {JOB_SLEEP_TIME_SECONDS} seconds.")
            time.sleep(JOB_SLEEP_TIME_SECONDS)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt called. Exiting.")
