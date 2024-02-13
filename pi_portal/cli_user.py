"""The Pi Portal User CLI."""

import click
from .cli_commands.cli_user import installer, version


@click.group()
@click.option('--debug', default=False, is_flag=True, help='Enable debug logs.')
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
  """Pi Portal User CLI."""

  ctx.ensure_object(dict)
  ctx.obj['DEBUG'] = debug


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


@cli.command("version")
def version_command() -> None:
  """Display the Pi Portal version."""

  command = version.VersionCommand()
  command.invoke()
