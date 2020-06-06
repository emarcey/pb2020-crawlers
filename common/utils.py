from urllib.parse import urlparse

from common.config import IMAGE_FORMATS


def clean_url(url: str) -> str:
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/{parsed_url.path}"


def url_is_image(url: str) -> bool:
    split_url = url.split(".")
    if len(split_url) == 0:
        return False

    if split_url[-1] in IMAGE_FORMATS:
        return True

    return False
