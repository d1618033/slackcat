"""
This module defines the CLI of slackcat
"""

import datetime

import click
from slack_sdk import WebClient

from ..cache import Cache, MessageCache
from ..config import config
from ..slack_iter import iter_messages
from ..utils import print_messages


@click.command(name="slackcat")
@click.option("--from-date", default=None)
@click.option("--channel", default=config.defaults.channel)
def main(from_date, channel):
    cache = MessageCache(Cache(config.cache.path))
    client = WebClient(token=config.credentials.token)
    if from_date is None:
        from_date = datetime.datetime.now() - datetime.timedelta(days=365)
    else:
        from_date = datetime.datetime.fromisoformat(from_date)
    if channel is None:
        raise click.ClickException("Channel cannot be empty")

    print_messages(
        iter_messages(
            client, from_date=from_date, channel=channel, cache=cache
        )
    )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
