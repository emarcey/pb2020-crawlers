import tweepy
from typing import Dict, List, Any, Set
from datetime import datetime

# from IPython import embed


from common.data_classes import RawSubmission
from common.enums import DataSource
from common.utils import write_raw_submissions_to_csv

# input your credentials here
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


QUERIES = [
    # recommended by freezman
    "#bluefall",
    # "#PoliceBrutality",
    # "#PoliceBrutailtyPandemic",
    # "#Protests2020",
    # cities by population - protests
    # "#nycProtests",
    # "#newyorkProtests",
    # "#losangelesProtests",
    # "#laprotests",
    # "#stLouisProtests",
    # "#stlProtests",
    # "#philadelphiaprotests",
    # "#phillyprotests",
    # "#chicagoprotests",
    # "#houstonprotests",
    # "#pheonixProtests",
    # "#miamiProtests",
    # "#dcprotests",
    # "#WashingtonDCProtest",
    # "#seattleprotest",
    # "#austinprotest"
    # # found from 949mac's endpoint https://api.846policebrutality.com/api/incidents?include=evidence
    # "#GeorgeFloyd",
    # "#JusticeForGeorgeFloyd",
    # "#AbolishThePolice",
    # "#BlackLivesMatter",
    # "tear gas",
]


def run_twitter_searches():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweets = []
    total_returned_tweets = 0
    processed_id_tweets = set()
    for query in QUERIES:
        cursor = query_twitter(api, query, 1270867714505158656)
        for resp in cursor:
            total_returned_tweets += 1
            tweet = resp._json
            submissions, processed_id_tweets = convert_tweet(tweet, processed_id_tweets)
            if not submissions:
                continue
            tweets.extend(submissions)
            if len(tweets) > 5:
                print("breaking out early for testing purposes")
                break
    print("total_returned_tweets", total_returned_tweets)
    write_raw_submissions_to_csv("tweet_submissions.csv", tweets)


def query_twitter(api, query: str, since_id: int):
    # TODO: include result_type? (mixed, recent, popular) probably want recent once batching is set up
    # TODO: why wasn't count working
    return tweepy.Cursor(api.search, q=query, lang="en", since_id=since_id, include_entities=True).items()


def convert_tweet(tweet: Dict[str, Any], processed_id_tweets: Set[int]):
    submissions = []
    # TODO: add "monetizable" logger. like, is somebody profiting off this shit?
    if not is_tweet_relevant(tweet):
        return None, processed_id_tweets
    if "retweeted_status" in tweet:
        tweet = tweet["retweeted_status"]
    id_tweet = tweet["id"]
    if id_tweet in processed_id_tweets:
        return None, processed_id_tweets
    processed_id_tweets.add(id_tweet)

    converted_date = twitter_created_at_to_utc(tweet["created_at"])
    submission_body = ""
    if tweet["geo"]:
        submission_body = f"Provided geo: {tweet['geo']}"
    elif tweet["user"].get("location"):
        submission_body = f"User Location: {tweet['user']['location']}"

    for media in tweet["extended_entities"]["media"]:
        if media["type"] != "video":
            continue
        print("found video for tweet\n", tweet["text"], "\n")

        media_url = get_media_url_from_variants(media["video_info"]["variants"])
        if not media_url:
            continue

        submission = RawSubmission(
            data_source=DataSource.twitter,
            id_source=id_tweet,
            submission_title=tweet["text"],
            submission_datetime_utc=converted_date,
            submission_community="",  # TODO: is this ok? I
            submission_url=media["expanded_url"],
            submission_media_url=media_url,
            submission_body=submission_body,
            id_submitter=tweet["user"]["id"],
        )
        submissions.append(submission)
    return submissions, processed_id_tweets


def is_tweet_relevant(tweet: Dict[str, Any]):
    media = tweet.get("extended_entities", {}).get("media")
    if media:
        return True
    # TODO: do we need a regex like reddit or is that handled by search params
    return False


def twitter_created_at_to_utc(created_at: str):
    # created at format: "Mon Aug 06 19:28:16 +0000 2018",
    return datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")


def get_media_url_from_variants(variants: List[Dict[str, str]]):
    for variant in variants:
        if variant["content_type"] == "video/mp4":
            # TODO: multiple bitrates are available, does it matter which?
            return variant["url"]
    return None


if __name__ == "__main__":
    run_twitter_searches()
