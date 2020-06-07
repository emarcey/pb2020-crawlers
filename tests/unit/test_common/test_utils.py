import pytest
from typing import Any, Set
from unittest.mock import Mock

from common.utils import clean_url, url_is_image, reddit_post_is_relevant


@pytest.mark.parametrize(
    "given, expected",
    [
        ("https://www.abc.com", "https://www.abc.com"),
        ("https://www.abc.com?s=21", "https://www.abc.com?s=21"),
        ("https://www.twitter.com", "https://www.twitter.com"),
        ("https://www.twitter.com?s=21", "https://www.twitter.com"),
    ],
)
def test_clean_url(given: str, expected: str) -> None:
    assert clean_url(given) == expected


@pytest.mark.parametrize(
    "given, expected",
    [
        ("https://www.abc.com", False),
        ("https://www.abc.com/blachdafh.gif", False),
        ("https://www.abc.com/blachdafh.png", True),
        ("https://www.abc.com/blachdafh.jpg", True),
        ("https://www.abc.com/blachdafh.jpeg", True),
        ("https://www.abc.com/blachdafh.jpeg.ssssike", False),
    ],
)
def test_url_is_image(given: str, expected: str) -> None:
    assert url_is_image(given) == expected


@pytest.mark.parametrize(
    "given_submission, given_explicit_subreddits, expected",
    [
        (Mock(is_self=True, stickied=False), set(), False),
        (Mock(is_self=True, stickied=True), set(), False),
        (Mock(is_self=False, stickied=True), set(), False),
        (Mock(is_self=False, stickied=False, media=None), set(), False),
        (Mock(is_self=False, stickied=False, media=Mock(), url="https://www.abc.com/blachdafh.jpg"), set(), False),
        (
            Mock(
                is_self=False,
                stickied=False,
                media=Mock(),
                url="https://www.abc.com/blachdafh.jpg",
                subreddit=Mock(display_name="dummy"),
            ),
            {"dummy"},
            False,
        ),
        (
            Mock(
                is_self=False,
                stickied=False,
                media=Mock(),
                url="https://www.abc.com/blachdafh",
                subreddit=Mock(display_name="dummy"),
                title="This is something basic",
            ),
            {"dummy"},
            True,
        ),
        (
            Mock(
                is_self=False,
                stickied=False,
                media=Mock(),
                url="https://www.abc.com/blachdafh",
                subreddit=Mock(display_name="dummy"),
                title="This is something basic",
            ),
            {"dummy2"},
            False,
        ),
        (
            Mock(
                is_self=False,
                stickied=False,
                media=Mock(),
                url="https://www.abc.com/blachdafh",
                subreddit=Mock(display_name="dummy"),
                title="something with cops",
            ),
            {"dummy2"},
            True,
        ),
    ],
)
def test_reddit_post_is_relevant(given_submission: Any, given_explicit_subreddits: Set[str], expected: bool) -> None:
    assert reddit_post_is_relevant(given_submission, given_explicit_subreddits) == expected
