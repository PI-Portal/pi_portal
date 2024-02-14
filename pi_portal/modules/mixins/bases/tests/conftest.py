"""Test fixtures for the mixins base class modules tests."""
# pylint: disable=redefined-outer-name

from typing import Type
from unittest import mock

import pytest
from pi_portal.modules.mixins.bases import write_log_file


@pytest.fixture
def mocked_get_logger() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_json_logger_config() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_log_file_writer_class(
    mocked_json_logger_config: mock.Mock,
) -> Type[write_log_file.LogFileWriterBase]:

  class ConcreteLogFileWriter(write_log_file.LogFileWriterBase):
    """A test class using the LogFileWriterBase mixin."""

    logging_config_class = mocked_json_logger_config
    logger_name = "test_archived_logger"
    log_file_path = "/var/run/some.log"

  return ConcreteLogFileWriter


@pytest.fixture
def concrete_log_file_writer_instance(
    concrete_log_file_writer_class: Type[write_log_file.LogFileWriterBase],
    mocked_get_logger: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> write_log_file.LogFileWriterBase:
  monkeypatch.setattr(
      write_log_file.__name__ + ".getLogger",
      mocked_get_logger,
  )
  return concrete_log_file_writer_class()
