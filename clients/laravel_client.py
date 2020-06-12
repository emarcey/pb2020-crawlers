from json import dumps
import requests
from typing import List

from common.config import LARAVEL_HOST, LARAVEL_ENDPOINT
from common.data_classes import RawSubmission


def bulk_upload_submissions(raw_submissions: List[RawSubmission], api_key: str) -> None:
    json_submissions = []
    for raw_submission in raw_submissions:
        json_submissions.append(raw_submission.to_dict())

    headers = {"Content-Type": "application/json", "Api-Token": api_key}

    resp = requests.post(
        url=f"{LARAVEL_HOST}/{LARAVEL_ENDPOINT}", data=dumps({"data": json_submissions}), headers=headers
    )
    if resp.status_code != 200:
        raise ValueError(f"Failed to upload to Laravel with resp: {resp.text}")
