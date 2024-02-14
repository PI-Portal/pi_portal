"""Test the ArchivedLogFileWriter mixin class."""

from pi_portal.modules.configuration.logging.json_archived import (
    JsonLoggerConfigurationArchived,
)
from ..bases.write_log_file import LogFileWriterBase
from ..write_archived_log_file import ArchivedLogFileWriter


class TestArchivedLogFileWriter:
  """Test the ArchivedLogFileWriter mixin class."""

  def test_initialize__attributes(
      self,
      log_file_archived_writer_instance: ArchivedLogFileWriter,
  ) -> None:
    assert log_file_archived_writer_instance.logging_config_class == (
        JsonLoggerConfigurationArchived
    )

  def test_initialize__inheritance(
      self,
      log_file_archived_writer_instance: ArchivedLogFileWriter,
  ) -> None:
    assert isinstance(
        log_file_archived_writer_instance,
        ArchivedLogFileWriter,
    )
    assert isinstance(
        log_file_archived_writer_instance,
        LogFileWriterBase,
    )
