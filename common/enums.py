from enum import Enum, unique


@unique
class DataSource(Enum):
    reddit = "Reddit"
    twitter = "Twitter"
