"""The Pi Portal CLI."""

import click
from .commands import (
    door_monitor,
    installer,
    slack_bot,
    upload_snapshot,
    upload_video,
)
from .modules.configuration import state


@click.group()
def cli() -> None:
  """Door Monitor CLI."""

  running_state = state.State()
  running_state.load()


@cli.command("monitor")
def monitor_command() -> None:
  """Begin monitoring the door."""

  command = door_monitor.DoorMonitorCommand()
  command.invoke()


@cli.command("slack_bot")
def slack_bot_command() -> None:
  """Connect the interactive Slack bot."""

  command = slack_bot.SlackBotCommand()
  command.invoke()


@cli.command("upload_snapshot")
@click.argument('filename', type=click.Path(exists=True))
def upload_snapshot_command(filename: str) -> None:
  """Upload a snapshot image to Slack.

  :param filename: The path to the file to upload.
  """

  command = upload_snapshot.UploadSnapshotCommand(filename)
  command.invoke()


@cli.command("upload_video")
@click.argument('filename', type=click.Path(exists=True))
def upload_video_command(filename: str) -> None:
  """Upload a video to Slack and S3.

  :param filename: The path to the file to upload.
  """

  command = upload_video.UploadVideoCommand(filename)
  command.invoke()


@cli.command("installer")
@click.argument('config_file', type=click.Path(exists=True))
def installer_command(config_file: str) -> None:
  """Run the installation script, (requires root).

  :param config_file: The path to the config file to use.
  """

  command = installer.InstallerCommand(config_file)
  command.invoke()
