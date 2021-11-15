"""The Pi Portal Door Monitor Application."""

import click
from . import config, modules


@click.group()
def cli() -> None:
  """Door Monitor CLI."""


@cli.command("monitor")
def monitor() -> None:
  """Begin monitoring the door."""
  door_monitor = modules.monitor.Monitor()
  door_monitor.log = modules.logger.setup_logger(
      door_monitor.log, config.LOGFILE_PATH
  )
  door_monitor.start()


@cli.command("slack_bot")
def slack_bot() -> None:
  """Connect the interactive Slack bot."""
  slack_client = modules.slack.Client()
  slack_client.subscribe()


@cli.command("upload_video")
@click.argument('filename', type=click.Path(exists=True))
def upload_video(filename: str) -> None:
  """Upload a video to Slack and S3."""
  slack_client = modules.slack.Client()
  slack_client.send_video(filename)


@cli.command("installer")
@click.argument('config_file', type=click.Path(exists=True))
def installer(config_file: str) -> None:
  """Run the installation script, (requires root)."""
  modules.installer.installer(config_file)
