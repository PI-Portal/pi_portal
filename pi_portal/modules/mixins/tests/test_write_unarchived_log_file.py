"""Test the UnarchivedLogFileWriter mixin class."""

from pi_portal.modules.configuration.logging.json_unarchived import (
    JsonLoggerConfigurationUnarchived,
)
from ..bases.write_log_file import LogFileWriterBase
from ..write_unarchived_log_file import UnarchivedLogFileWriter


class TestUnarchivedLogFileWriter:
  """Test the UnarchivedLogFileWriter mixin class."""

  def test_initialize__attributes(
      self,
      log_file_unarchived_writer_instance: UnarchivedLogFileWriter,
  ) -> None:
    assert log_file_unarchived_writer_instance.logging_config_class == (
        JsonLoggerConfigurationUnarchived
    )

  def test_initialize__inheritance(
      self,
      log_file_unarchived_writer_instance: UnarchivedLogFileWriter,
  ) -> None:
    assert isinstance(
        log_file_unarchived_writer_instance,
        UnarchivedLogFileWriter,
    )
    assert isinstance(
        log_file_unarchived_writer_instance,
        LogFileWriterBase,
    )
