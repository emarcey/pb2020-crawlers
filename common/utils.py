from common.config import IMAGE_FORMATS


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
