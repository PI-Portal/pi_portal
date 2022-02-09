"""The Pi Portal CLI."""

import click
from .commands import (
    door_monitor,
    installer,
    slack_bot,
    upload_snapshot,
    upload_video,
    version,
)


@click.group()
@click.option('--debug', default=False, is_flag=True, help='Enable debug logs.')
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
  """Door Monitor CLI."""

  ctx.ensure_object(dict)
  ctx.obj['DEBUG'] = debug


@cli.command("monitor")
@click.pass_context
def monitor_command(ctx: click.Context) -> None:
  """Begin monitoring the door."""

  command = door_monitor.DoorMonitorCommand()
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()


@cli.command("slack_bot")
@click.pass_context
def slack_bot_command(ctx: click.Context) -> None:
  """Connect the interactive Slack bot."""

  command = slack_bot.SlackBotCommand()
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()


@cli.command("upload_snapshot")
@click.argument('filename', type=click.Path(exists=True))
@click.pass_context
def upload_snapshot_command(ctx: click.Context, filename: str) -> None:
  """Upload a snapshot image to Slack.

  FILENAME: The path to the image file to upload.
  """

  command = upload_snapshot.UploadSnapshotCommand(filename)
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()


@cli.command("upload_video")
@click.argument('filename', type=click.Path(exists=True))
@click.pass_context
def upload_video_command(ctx: click.Context, filename: str) -> None:
  """Upload a video to Slack and S3.

  FILENAME: The path to the video file to upload.
  """

  command = upload_video.UploadVideoCommand(filename)
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()


@cli.command("installer")
@click.argument('config_file', type=click.Path(exists=True))
def installer_command(config_file: str) -> None:
  """Run the installation script, (requires root).

  CONFIG_FILE: The path to the configuration file to use.
  """

  command = installer.InstallerCommand(config_file)
  command.invoke()


@cli.command("version")
def version_command() -> None:
  """Display the Pi Portal version."""

  command = version.VersionCommand()
  command.invoke()
