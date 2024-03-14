"""Shared fixtures for the installer modules tests."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO

import pytest
from pi_portal.modules.configuration.logging import installer


@pytest.fixture
def mocked_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def installer_logger_stdout(mocked_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test_installer")
  installer.InstallerLoggerConfiguration().configure(logger)
  handler = logging.StreamHandler(stream=mocked_stream)
  handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  return logger
