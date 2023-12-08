"""StepKillMotion class."""

import os

from .bases import process_step, system_call_step


class StepKillMotion(
    process_step.ProcessStepBase,
    system_call_step.SystemCallBase,
):
  """Kill the motion process and remove it from startup."""

  def invoke(self) -> None:
    """Kill the motion process and remove it from startup."""

    self.log.info("Killing the motion process ...")
    if os.path.exists(self.pid_file_path):
      self.process.kill()
    else:
      self.log.info("No motion process to kill.")
    self.log.info("Done killing the motion process.")

    self.log.info("Removing motion from startup ...")
    self._system_call("update-rc.d -f motion remove")
    self.log.info("Done removing motion from startup.")
