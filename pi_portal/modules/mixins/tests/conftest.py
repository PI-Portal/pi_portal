"""Test fixtures for the mixins modules tests."""

import pytest
from pi_portal.modules.configuration.tests.fixtures import mock_state
from .. import read_log_file


class ClassWithLoggingReader(read_log_file.LogFileReader):
  """A test class using the ReadLogFile mixin."""

  logger_name = "test_logger"
  log_file_path = "/var/run/some.log"


@pytest.fixture
@mock_state.patch
def instance() -> ClassWithLoggingReader:
  """Test double for the temperature monitor logfile."""

  return ClassWithLoggingReader()
