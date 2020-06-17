from datadog import initialize
import logging
import os
import time

from common.config import DATADOG_OPTIONS, JOB_SLEEP_TIME_SECONDS, READER_MODE
from reddit.feed_reader import run_reddit_feed

logging.basicConfig()
logging.root.setLevel(logging.INFO)


logger = logging.getLogger(__name__)

initialize(**DATADOG_OPTIONS)


if __name__ == "__main__":
    try:
        while True:
            if READER_MODE == "reddit":
                run_reddit_feed()
            else:
                raise ValueError(f"READER_MODE {READER_MODE} not supported")
            logger.info(f"Job complete. Sleeping for {JOB_SLEEP_TIME_SECONDS} seconds.")
            time.sleep(JOB_SLEEP_TIME_SECONDS)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt called. Exiting.")
