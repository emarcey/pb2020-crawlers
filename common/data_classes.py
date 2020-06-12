from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from common.config import DATE_TIME_FORMAT
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
    submission_media_url: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data_source": self.data_source.value,
            "id_source": self.id_source,
            "submission_community": self.submission_community,
            "submission_datetime_utc": self.submission_datetime_utc.strftime(DATE_TIME_FORMAT),
            "submission_title": self.submission_title,
            "submission_body": self.submission_body,
            "id_submitter": self.id_submitter,
            "submission_url": self.submission_url,
            "submission_media_url": self.submission_media_url,
        }
