"""StepKillSupervisor class."""

import os

from .bases import process_step


class StepKillSupervisor(process_step.ProcessStepBase):
  """Kill the supervisor process."""

  def invoke(self) -> None:
    """Kill the supervisor process."""

    self.log.info("Killing the supervisor process ...")
    if os.path.exists(self.pid_file_path):
      self.process.kill()
    else:
      self.log.info("No supervisor process to kill.")
    self.log.info("Done killing the supervisor process.")
