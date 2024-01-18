"""Pi Portal Machine CLI."""

import click
from .cli_commands.cli_machine import task_scheduler


@click.group()
@click.option('--debug', default=False, is_flag=True, help='Enable debug logs.')
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
  """Pi Portal Machine CLI."""

  ctx.ensure_object(dict)
  ctx.obj['DEBUG'] = debug


@cli.command("task_scheduler")
@click.pass_context
def task_scheduler_command(ctx: click.Context) -> None:
  """Start the task scheduler."""

  command = task_scheduler.TaskSchedulerCommand()
  command.load_state(debug=ctx.obj['DEBUG'])
  command.invoke()
