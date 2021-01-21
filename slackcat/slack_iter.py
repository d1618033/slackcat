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
    to_date: datetime.datetime,
    from_date: datetime.datetime,
) -> Iterable[Message]:
    latest = to_date.timestamp()
    for _ in range(MAX_ITERATIONS):
        conversations = client.conversations_history(
            channel=channel, latest=latest, limit=LIMIT
        )
        assert isinstance(conversations.data, dict)
        messages = [
            Message(**message) for message in conversations.data["messages"]
        ]
        if not messages:
            return
        for message in messages:
            if message.ts.timestamp() < from_date.timestamp():
                return
            yield message
        latest = messages[-1].ts.timestamp()


def _cache_messages(
    messages: Iterable[Message], cache: MessageCache
) -> Iterable[Message]:
    for message in messages:
        cache.add(message)
        yield message
    cache.sync()


def iter_messages(
    client: WebClient,
    *,
    channel: str,
    from_date: datetime.datetime,
    cache: MessageCache,
) -> Iterable[Message]:
    now = datetime.datetime.now()
    messages = cache.get_in_range(from_date, now)
    yield from _cache_messages(
        messages=_fetch_messages(
            client,
            channel=channel,
            to_date=now,
            from_date=messages[-1].ts + datetime.timedelta(milliseconds=1),
        ),
        cache=cache,
    )
    yield from reversed(messages)
    yield from _cache_messages(
        messages=_fetch_messages(
            client,
            channel=channel,
            to_date=messages[0].ts,
            from_date=from_date,
        ),
        cache=cache,
    )
