"""StepEnsureRoot class."""

import os

from .bases import base_step


class StepEnsureRoot(base_step.StepBase):
  """Ensure that the installer is running as root."""

  insufficient_privileges_msg: str = \
      "The pi_portal configuration installer must be run as root."

  def invoke(self) -> None:
    """Ensure that the installer is running as root."""

    self.log.info("Ensuring that the installer is running as root ...")
    if os.geteuid() != 0:
      self.log.error("This installer must be run as root!")
      raise PermissionError(self.insufficient_privileges_msg)
    self.log.info("Done ensuring that the installer is running as root.")
