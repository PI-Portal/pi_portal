"""Test the WriteLogFile mixin classes."""

from unittest import TestCase, mock

from .. import log_file

LOG_FILE_MODULE = log_file.__name__


class ClassWithLogging(log_file.WriteLogFile):
  """A test class using the WriteLogFile mixin."""

  logger_name = "test_logger"
  log_file_path = "/var/run/some.log"


@mock.patch(LOG_FILE_MODULE + '.getLogger')
@mock.patch(LOG_FILE_MODULE + '.logger.LoggingConfiguration')
class WriteLogFileTest(TestCase):
  """Test the WriteLogFile mixin class."""

  def setUp(self) -> None:
    self.instance = ClassWithLogging()

  def test_configure_logger(
      self,
      m_config: mock.Mock,
      m_get: mock.Mock,
  ) -> None:

    self.instance.configure_logger()

    m_get.assert_called_once_with(self.instance.logger_name)
    m_config.assert_called_once_with()
    m_config.return_value.configure.assert_called_once_with(
        m_get.return_value, self.instance.log_file_path
    )

    self.assertEqual(self.instance.log, m_get.return_value)
