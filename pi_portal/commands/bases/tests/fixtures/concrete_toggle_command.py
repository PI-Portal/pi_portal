"""ConcreteToggleCommand class."""

from pi_portal.commands.bases import toggle_command


class ConcreteToggleCommand(toggle_command.ToggleCommandBase):
  """Concrete implementation of the ToggleCommandBase class."""

  def invoke(self) -> None:
    """Invoke this command."""

    print("invoked ConcreteToggleCommand!")
