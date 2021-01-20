import datetime
from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Message(BaseModel):
    ts: datetime.datetime
    text: str
    type: Optional[str] = None
    subtype: Optional[str] = None
    user: Optional[str] = None
    inviter: Optional[str] = None

    def __str__(self):
        return f"{self.ts.isoformat()} {self.text!r}"
