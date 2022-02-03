"""The Pi Portal CLI."""

import click
from . import config
from .modules import configuration, integrations, system


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
  """Door Monitor CLI.

  :param ctx: The passed click context object.
  """

  running_state = configuration.state.State()
  running_state.load()
  ctx.obj = {
      'running_state': running_state,
      'logging_config': configuration.LoggingConfiguration()
  }


@cli.command("monitor")
@click.pass_context
def monitor(ctx: click.Context) -> None:
  """Begin monitoring the door.

  :param ctx: The passed click context object.
  """

  door_monitor = integrations.door_monitor.DoorMonitor()
  door_monitor.log = ctx.obj['logging_config'].configure(
      door_monitor.log,
      config.LOGFILE_PATH,
  )
  door_monitor.start()


@cli.command("slack_bot")
def slack_bot() -> None:
  """Connect the interactive Slack bot."""

  slack_client = integrations.slack.Client()
  slack_client.subscribe()


@cli.command("upload_snapshot")
@click.argument('filename', type=click.Path(exists=True))
def upload_snapshot(filename: str) -> None:
  """Upload a snapshot image to Slack.

  :param filename: The path to the file to upload.
  """

  slack_client = integrations.slack.Client()
  slack_client.send_snapshot(filename)


@cli.command("upload_video")
@click.argument('filename', type=click.Path(exists=True))
def upload_video(filename: str) -> None:
  """Upload a video to Slack and S3.

  :param filename: The path to the file to upload.
  """

  slack_client = integrations.slack.Client()
  slack_client.send_video(filename)


@cli.command("installer")
@click.argument('config_file', type=click.Path(exists=True))
def installer(config_file: str) -> None:
  """Run the installation script, (requires root).

  :param config_file: The path to the config file to use.
  """

  system.installer.installer(config_file)
