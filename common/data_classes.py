from dataclasses import dataclass
from datetime import datetime

from common.enums import DataSource


@dataclass
class RawSubmission:
    data_source: DataSource
    id_source: str
    submission_community: str
    submission_datetime_utc: datetime
    submission_title: str
    submission_body: str
    id_submitter: str
    submission_url: str
    submission_media_urls: str
