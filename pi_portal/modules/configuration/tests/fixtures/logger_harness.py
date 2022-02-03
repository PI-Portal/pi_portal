"""Test harness for the LoggerConfiguration class."""

import logging
from unittest import TestCase

from pi_portal.modules.configuration import logger, state


class LoggingConfigurationTestHarness(TestCase):
  """Test harness for the LoggerConfiguration class."""

  logger_name: str

  def get_logger(self) -> logging.Logger:
    return logging.getLogger(self.logger_name)

  def setUp(self) -> None:
    self.state = state.State()
    self.logging_configuration = logger.LoggingConfiguration()
