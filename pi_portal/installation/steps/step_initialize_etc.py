"""StepInitializeEtc class."""

import os

from .bases import system_call_step


class StepInitializeEtc(system_call_step.SystemCallBase):
  """Initialize etc paths for system dependencies."""

  etc_paths = [
      "/etc/filebeat",
      "/etc/motion",
      "/etc/pki/tls/certs",
  ]

  def invoke(self) -> None:
    """Initialize etc paths for system dependencies."""

    self.log.info("Initializing etc paths ...")

    for etc_path in self.etc_paths:

      self.log.info("Creating '%s' ...", etc_path)
      if not os.path.exists(etc_path):
        self._system_call(f"mkdir -p {etc_path}")
      else:
        self.log.info("Found existing '%s' ...", etc_path)

      self.log.info("Setting permissions on '%s' ...", etc_path)
      self._system_call(f"chown root:root {etc_path}")
      self._system_call(f"chmod 755 {etc_path}")

    self.log.info("Done initializing etc paths.")
