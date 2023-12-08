"""Installs the end user's pi_portal configuration."""

import logging
from typing import List

from pi_portal import config
from pi_portal.modules.configuration.logging import installer
from .steps import (
    StepEnsureRoot,
    StepInitializeLogging,
    StepInstallConfigFile,
    StepKillMotion,
    StepKillSupervisor,
    StepRenderTemplates,
    StepStartSupervisor,
)
from .steps.bases import base_step


class Installer:
  """Installs the end user's pi_portal configuration."""

  steps: List[base_step.StepBase]
  config_file_path: str
  logger_name: str = "Installer"
  logger_level: int = logging.INFO

  def __init__(self, config_file_path: str) -> None:
    self.log = logging.getLogger(self.logger_name)
    logger_configuration = installer.InstallerLoggerConfiguration()
    logger_configuration.configure(self.log)
    self.config_file_path = config_file_path
    self.log.setLevel(self.logger_level)
    self.steps = self._configure_steps()

  def _configure_steps(self) -> List[base_step.StepBase]:
    return [
        StepEnsureRoot(self.log),
        StepKillMotion(self.log, config.PID_FILE_MOTION),
        StepKillSupervisor(self.log, config.PID_FILE_SUPERVISORD),
        StepInitializeLogging(self.log),
        StepRenderTemplates(self.log),
        StepInstallConfigFile(self.log, self.config_file_path),
        StepStartSupervisor(self.log),
    ]

  def install(self) -> None:
    """Installs the end user's pi_portal configuration."""

    self.log.info("Beginning installation ...")

    for step in self.steps:
      step.invoke()

    self.log.info("Installation complete.")
