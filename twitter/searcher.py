import tweepy
from IPython import embed

# import csv

# import pandas as pd

# ###input your credentials here
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
# ####United Airlines
# Open/Create a file to append data
# csvFile = open("ua.csv", "a")
# Use csv Writer
# csvWriter = csv.writer(csvFile)

queries = [
    # recommended by freezman
    "#bluefall",
    "#PoliceBrutailtyPandemic",
    "#PoliceBrutality",
    "#Protests2020",
    # cities by population - protests
    "#nycProtests",
    "#newyorkProtests",
    "#losangelesProtests",
    "#laprotests",
    "#stLouisProtests",
    "#stlProtests",
    "#philadelphiaprotests",
    "#phillyprotests",
    "#chicagoprotests",
    "#houstonprotests",
    "#pheonixProtests",
    "#miamiProtests",
    "#dcprotests",
    "#WashingtonDCProtest",
    "#seattleprotest",
    "#austinprotest"
    # found from 949mac's endpoint https://api.846policebrutality.com/api/incidents?include=evidence
    "#GeorgeFloyd",
    "#JusticeForGeorgeFloyd",
    "#AbolishThePolice",
    "#BlackLivesMatter",
    "tear gas",
]

# TODO: should we include filter:images
for tweet in tweepy.Cursor(
    api.search, q="#blm", count=3, lang="en", since="2020-05-25", include_entities=True, filter="videos"
).items():
    media = tweet._json["entities"]["media"]
    embed()
    return
