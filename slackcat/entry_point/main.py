"""
This module defines the CLI of slackcat
"""

import datetime
import sys

import click
from slack_sdk import WebClient

from ..cache import Cache
from ..config import config
from ..slack_iter import iter_messages


@click.command(name="slackcat")
@click.option("--from-date", default=None)
@click.option("--channel", default=config.defaults.channel)
def main(from_date, channel):
    cache = Cache(config.cache.path)
    client = WebClient(token=config.credentials.token)
    if from_date is None:
        from_date = datetime.datetime.now() - datetime.timedelta(days=365)
    else:
        from_date = datetime.datetime.fromisoformat(from_date)
    if channel is None:
        raise click.ClickException("Channel cannot be empty")

    for message in iter_messages(
        client, from_date=from_date, channel=channel, cache=cache
    ):
        try:
            print(message, flush=True)
        except (BrokenPipeError, IOError):
            sys.stderr.close()
            return


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
