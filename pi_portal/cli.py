"""The Pi Portal CLI."""

import click
from .modules import configuration, integrations, system


@click.group()
def cli() -> None:
  """Door Monitor CLI."""

  running_state = configuration.state.State()
  running_state.load()


@cli.command("monitor")
def monitor() -> None:
  """Begin monitoring the door."""

  factory = integrations.gpio.DoorMonitorFactory()
  door_monitor = factory.create()
  door_monitor.start()


@cli.command("slack_bot")
def slack_bot() -> None:
  """Connect the interactive Slack bot."""

  rtm_bot = integrations.slack.SlackBot()
  rtm_bot.connect()


@cli.command("upload_snapshot")
@click.argument('filename', type=click.Path(exists=True))
def upload_snapshot(filename: str) -> None:
  """Upload a snapshot image to Slack.

  :param filename: The path to the file to upload.
  """

  slack_client = integrations.slack.SlackClient()
  slack_client.send_snapshot(filename)


@cli.command("upload_video")
@click.argument('filename', type=click.Path(exists=True))
def upload_video(filename: str) -> None:
  """Upload a video to Slack and S3.

  :param filename: The path to the file to upload.
  """

  slack_client = integrations.slack.SlackClient()
  slack_client.send_video(filename)


@cli.command("installer")
@click.argument('config_file', type=click.Path(exists=True))
def installer(config_file: str) -> None:
  """Run the installation script, (requires root).

  :param config_file: The path to the config file to use.
  """

  system.installer.installer(config_file)
