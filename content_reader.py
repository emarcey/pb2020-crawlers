import os
import time

from common.config import JOB_SLEEP_TIME_SECONDS, READER_MODE
from reddit_rss.feed_reader import run_reddit_rss_feed


if __name__ == "__main__":
    try:
        while True:
            if READER_MODE == "reddit":
                run_reddit_rss_feed()
            else:
                raise ValueError(f"READER_MODE {READER_MODE} not supported")
            print(f"Job complete. Sleeping for {JOB_SLEEP_TIME_SECONDS} seconds.")
            time.sleep(JOB_SLEEP_TIME_SECONDS)
    except KeyboardInterrupt:
        print("KeyboardInterrupt called. Exiting.")
