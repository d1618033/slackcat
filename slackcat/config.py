from pathlib import Path
from typing import Optional

import toml
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Credentials(BaseModel):
    token: str


class Defaults(BaseModel):
    channel: Optional[str] = None


class Requests(BaseModel):
    limit_per_request: int = 10
    max_number_requests: int = 1000


class Cache(BaseModel):
    path: Path = Path.home() / ".slackcat" / "cache"


class Config(BaseModel):
    defaults: Defaults
    credentials: Credentials
    requests: Requests
    cache: Cache


config = Config(**toml.load(Path.home() / ".slackcat" / "config.toml"))
