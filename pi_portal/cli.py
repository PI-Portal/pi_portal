"""The Pi Portal Door Monitor Application."""

import click
from . import config, modules


@click.group()
def cli():
  """Door Monitor CLI."""


@cli.command("monitor")
def monitor():
  """Begin monitoring the door."""
  modules.state.State().load()
  door_monitor = modules.monitor.Monitor()
  door_monitor.log = modules.logger.setup_logger(
      door_monitor.log, config.LOGFILE_PATH
  )
  door_monitor.start()


@cli.command("slack_bot")
def slack_bot():
  """Connect the interactive Slack bot."""
  modules.state.State().load()
  slack_client = modules.slack.Client()
  slack_client.subscribe()


@cli.command("upload_video")
@click.argument('filename', type=click.Path(exists=True))
def upload_video(filename: str):
  """Upload a video to Slack and S3.

  :param filename: The path to the file to upload.
  """

  modules.state.State().load()
  slack_client = modules.slack.Client()
  slack_client.send_video(filename)


@cli.command("installer")
@click.argument('config_file', type=click.Path(exists=True))
def installer(config_file: str):
  """Run the installation script, (requires root).

  :param config_file: The path to the config file to use.
  """

  modules.installer.installer(config_file)
