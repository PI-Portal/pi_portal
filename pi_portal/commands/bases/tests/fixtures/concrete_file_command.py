"""ConcreteFileCommand class."""

from pi_portal.commands.bases import file_command


class ConcreteFileCommand(file_command.FileCommandBase):
  """Concrete implementation of the FileCommandBase class."""

  def invoke(self) -> None:
    """Invoke this command."""

    print("invoked ConcreteFileCommand!")
