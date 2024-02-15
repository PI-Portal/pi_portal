"""Pi Portal Machine CLI."""

import click
from .cli_commands.cli_machine import (
    contact_switch_monitor,
    slack_bot,
    task_scheduler,
    temperature_monitor,
    upload_snapshot,
    upload_video,
)


@click.group()
@click.option('--debug', default=False, is_flag=True, help='Enable debug logs.')
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
  """Pi Portal Machine CLI."""

  ctx.ensure_object(dict)
  ctx.obj['DEBUG'] = debug


@cli.command("contact_switch_monitor")
@click.pass_context
def contact_switch_monitor_command(ctx: click.Context) -> None:
  """Start the contact switch monitor."""

  command = contact_switch_monitor.ContactSwitchMonitorCommand()
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()


@cli.command("slack_bot")
@click.pass_context
def slack_bot_command(ctx: click.Context) -> None:
  """Connect the interactive Slack bot."""

  command = slack_bot.SlackBotCommand()
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()


@cli.command("task_scheduler")
@click.pass_context
def task_scheduler_command(ctx: click.Context) -> None:
  """Start the task scheduler."""

  command = task_scheduler.TaskSchedulerCommand()
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
