"""The Pi Portal Door DoorMonitor Application."""

import click
from . import config
from .modules import configuration, general, integrations, system


@click.group()
def cli():
  """Door Monitor CLI."""


@cli.command("monitor")
def monitor():
  """Begin monitoring the door."""
  configuration.state.State().load()
  door_monitor = integrations.door_monitor.DoorMonitor()
  door_monitor.log = general.logger.setup_logger(
      door_monitor.log, config.LOGFILE_PATH
  )
  door_monitor.start()


@cli.command("slack_bot")
def slack_bot():
  """Connect the interactive Slack bot."""
  configuration.state.State().load()
  slack_client = integrations.slack.Client()
  slack_client.subscribe()


@cli.command("upload_snapshot")
@click.argument('filename', type=click.Path(exists=True))
def upload_snapshot(filename: str):
  """Upload a snapshot image to Slack.

  :param filename: The path to the file to upload.
  """

  configuration.state.State().load()
  slack_client = integrations.slack.Client()
  slack_client.send_snapshot(filename)


@cli.command("upload_video")
@click.argument('filename', type=click.Path(exists=True))
def upload_video(filename: str):
  """Upload a video to Slack and S3.

  :param filename: The path to the file to upload.
  """

  configuration.state.State().load()
  slack_client = integrations.slack.Client()
  slack_client.send_video(filename)


@cli.command("installer")
@click.argument('config_file', type=click.Path(exists=True))
def installer(config_file: str):
  """Run the installation script, (requires root).

  :param config_file: The path to the config file to use.
  """

  system.installer.installer(config_file)
