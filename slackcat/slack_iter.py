import datetime
from typing import Iterable

from slack_sdk import WebClient

from .cache import MessageCache
from .config import config
from .message import Message

MAX_ITERATIONS = config.requests.max_number_requests
LIMIT = config.requests.limit_per_request


def _fetch_messages(
    client: WebClient,
    *,
    channel: str,
    latest: float,
) -> Iterable[Message]:
    for _ in range(MAX_ITERATIONS):
        conversations = client.conversations_history(
            channel=channel, latest=latest, limit=LIMIT
        )
        assert isinstance(conversations.data, dict)
        messages = [
            Message(**message) for message in conversations.data["messages"]
        ]
        for message in messages:
            yield message
        latest = messages[-1].ts.timestamp()


def iter_messages(
    client: WebClient,
    *,
    channel: str,
    from_date: datetime.datetime,
    cache: MessageCache,
) -> Iterable[Message]:
    now = datetime.datetime.now()
    if messages := cache.get_in_range(from_date, now):
        yield from reversed(messages)
        latest = messages[0].ts.timestamp()
    else:
        latest = now.timestamp()
    for message in _fetch_messages(client, channel=channel, latest=latest):
        if message.ts.timestamp() < from_date.timestamp():
            break
        cache.add(message)
        yield message
    cache.sync()

