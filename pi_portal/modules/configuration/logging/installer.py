"""InstallerLoggerConfiguration class."""

import logging

from .bases.base_logger import LoggerConfigurationBase


class InstallerLoggerConfiguration(LoggerConfigurationBase):
  """Installer logger configuration."""

  format_str = '%(name)s - %(levelname)s - %(message)s'

  def configure_formatter(self) -> None:
    """Configure the logger's formatter."""

    self.formatter = logging.Formatter(self.format_str)
