from click.testing import CliRunner

from slackcat.entry_point.main import main


def test_main():
    runner = CliRunner()
    assert runner.invoke(main, ["--help"]).stdout.startswith("Usage: slackcat")
