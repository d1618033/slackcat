from slackcat.entry_point.main import main
from click.testing import CliRunner


def test_main():
    runner = CliRunner()
    assert runner.invoke(main, ["--help"]).stdout.startswith("Usage: slackcat")

