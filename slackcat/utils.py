import sys
from typing import List, Protocol


class Stringable(Protocol):
    def __str__(self) -> str:
        ...


def print_messages(messages: List[Stringable]):
    for message in messages:
        try:
            print(message, flush=True)
        except (BrokenPipeError, IOError):
            sys.stderr.close()
            return
