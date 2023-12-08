"""StepStartSupervisor class."""

from .bases import system_call_step


class StepStartSupervisor(system_call_step.SystemCallBase):
  """Start the supervisor process."""

  def invoke(self) -> None:
    """Start the supervisor process."""

    self.log.info("Starting the supervisor process ...")
    self._system_call("service supervisor start")
    self.log.info("Done starting the supervisor process.")
