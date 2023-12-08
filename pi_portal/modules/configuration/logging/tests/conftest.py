"""Shared fixtures for the formatters modules."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO

import pytest
from pi_portal.modules.configuration.tests.fixtures import mock_state
from ..installer import InstallerLoggerConfiguration
from ..json import JsonLoggerConfiguration


@pytest.fixture
def installer_logger_configuration_instance() -> InstallerLoggerConfiguration:
  with mock_state.mock_state_creator():
    return InstallerLoggerConfiguration()


@pytest.fixture
def installer_logger_stdout_instance(
    monkeypatch: pytest.MonkeyPatch,
    installer_logger_configuration_instance: InstallerLoggerConfiguration,
    mocked_logger_name: str,
    mocked_stream: StringIO,
) -> logging.Logger:
  log = logging.getLogger(mocked_logger_name)
  installer_logger = installer_logger_configuration_instance
  installer_logger.configure(log)
  monkeypatch.setattr(log.handlers[0], "stream", mocked_stream)
  return log


@pytest.fixture
def json_logger_configuration_instance() -> JsonLoggerConfiguration:
  with mock_state.mock_state_creator():
    return JsonLoggerConfiguration()


@pytest.fixture
def json_logger_stdout_instance(
    monkeypatch: pytest.MonkeyPatch,
    json_logger_configuration_instance: JsonLoggerConfiguration,
    mocked_logger_name: str,
    mocked_stream: StringIO,
) -> logging.Logger:
  log = logging.getLogger(mocked_logger_name)
  json_logger = json_logger_configuration_instance
  json_logger.configure(log)
  monkeypatch.setattr(log.handlers[0], "stream", mocked_stream)
  return log
