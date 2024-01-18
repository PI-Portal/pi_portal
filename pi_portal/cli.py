"""The Pi Portal User CLI."""

import click
from .cli_commands import (
    door_monitor,
    installer,
    slack_bot,
    temperature_monitor,
    upload_snapshot,
    upload_video,
    version,
)


@click.group()
@click.option('--debug', default=False, is_flag=True, help='Enable debug logs.')
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
  """Pi Portal User CLI."""

  ctx.ensure_object(dict)
  ctx.obj['DEBUG'] = debug


@cli.command("door_monitor")
@click.pass_context
def door_monitor_command(ctx: click.Context) -> None:
  """Start the door monitor."""

  command = door_monitor.DoorMonitorCommand()
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()


@cli.command("install_config")
@click.option(
    '-y',
    '--yes',
    'confirmation',
    default=False,
    is_flag=True,
    help='Answer "yes" to installation confirmation.',
)
@click.argument('config_file', type=click.Path(exists=True))
@click.pass_context
def installer_command(
    ctx: click.Context, confirmation: bool, config_file: str
) -> None:
  """Install a configuration file. Requires root.

  CONFIG_FILE: The path to the configuration file to use.
  """

  command = installer.InstallerCommand(config_file, confirmation)
  command.load_state(debug=ctx.obj['DEBUG'], file_path=config_file)
  command.invoke()


@cli.command("slack_bot")
@click.pass_context
def slack_bot_command(ctx: click.Context) -> None:
  """Connect the interactive Slack bot."""

  command = slack_bot.SlackBotCommand()
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()


@cli.command("temp_monitor")
@click.pass_context
def temp_monitor_command(ctx: click.Context) -> None:
  """Start the temperature monitor."""

  command = temperature_monitor.TemperatureMonitorCommand()
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


@cli.command("version")
def version_command() -> None:
  """Display the Pi Portal version."""

  command = version.VersionCommand()
  command.invoke()
