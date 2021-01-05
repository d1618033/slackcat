"""
This module defines the CLI of slackcat
"""

import datetime
import sys
from pathlib import Path
from typing import Optional

import click
import toml
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from slack_sdk import WebClient

MAX_ITERATIONS = 1000
LIMIT = 10


class Message(BaseModel):
    ts: datetime.datetime
    text: str
    type: Optional[str] = None
    subtype: Optional[str] = None
    user: Optional[str] = None
    inviter: Optional[str] = None

    def __str__(self):
        return f"{self.ts.isoformat()} {self.text!r}"


@click.command(name="slackcat")
@click.option("--from-date", default=None)
@click.option("--channel", required=True)
def main(from_date, channel):
    config = toml.load(Path.home() / ".slackcat.toml")
    client = WebClient(token=config["credentials"]["token"])
    latest = datetime.datetime.now().timestamp()
    if from_date is None:
        from_date = datetime.datetime.now() - datetime.timedelta(days=365)
    else:
        from_date = datetime.datetime.fromisoformat(from_date)
    for _ in range(MAX_ITERATIONS):
        conversations = client.conversations_history(
            channel=channel, latest=latest, limit=LIMIT
        )
        messages = [
            Message(**message) for message in conversations.data["messages"]
        ]
        for message in messages:
            if message.ts.timestamp() < from_date.timestamp():
                return
            try:
                print(message, flush=True)
            except (BrokenPipeError, IOError):
                sys.stderr.close()
                return


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
