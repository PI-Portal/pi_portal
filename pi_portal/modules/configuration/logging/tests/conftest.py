"""Shared fixtures for the formatters modules."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO

import pytest
from pi_portal.modules.configuration.tests.fixtures import mock_state
from ..installer import InstallerLoggerConfiguration
from ..json_archived import JsonLoggerConfigurationArchived
from ..json_unarchived import JsonLoggerConfigurationUnarchived


@pytest.fixture
def installer_logger_configuration_instance() -> InstallerLoggerConfiguration:
  with mock_state.mock_state_creator():
    return InstallerLoggerConfiguration()


@pytest.fixture
def installer_logger_stdout_instance(
    monkeypatch: pytest.MonkeyPatch,
    installer_logger_configuration_instance: InstallerLoggerConfiguration,
    mocked_logger_name: str,
    mocked_logger_stream: StringIO,
) -> logging.Logger:
  log = logging.getLogger(mocked_logger_name)
  installer_logger = installer_logger_configuration_instance
  installer_logger.configure(log)
  monkeypatch.setattr(log.handlers[0], "stream", mocked_logger_stream)
  return log


@pytest.fixture
def archived_json_logger_instance() -> JsonLoggerConfigurationArchived:
  with mock_state.mock_state_creator():
    return JsonLoggerConfigurationArchived()


@pytest.fixture
def archived_json_logger_stdout_instance(
    monkeypatch: pytest.MonkeyPatch,
    archived_json_logger_instance: JsonLoggerConfigurationArchived,
    mocked_logger_name: str,
    mocked_logger_file_name: str,
    mocked_logger_stream: StringIO,
) -> logging.Logger:
  log = logging.getLogger(mocked_logger_name)
  json_logger = archived_json_logger_instance
  json_logger.configure(log, mocked_logger_file_name)
  monkeypatch.setattr(log.handlers[0], "stream", mocked_logger_stream)
  return log


@pytest.fixture
def unarchived_json_logger_instance() -> JsonLoggerConfigurationUnarchived:
  with mock_state.mock_state_creator():
    return JsonLoggerConfigurationUnarchived()


@pytest.fixture
def unarchived_json_logger_stdout_instance(
    monkeypatch: pytest.MonkeyPatch,
    unarchived_json_logger_instance: JsonLoggerConfigurationUnarchived,
    mocked_logger_name: str,
    mocked_logger_file_name: str,
    mocked_logger_stream: StringIO,
) -> logging.Logger:
  log = logging.getLogger(mocked_logger_name)
  json_logger = unarchived_json_logger_instance
  json_logger.configure(log, mocked_logger_file_name)
  monkeypatch.setattr(log.handlers[0], "stream", mocked_logger_stream)
  return log
