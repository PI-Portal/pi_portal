"""Test the RotatingFileHandlerUnarchived class."""

import logging
import logging.handlers

from ..rotation_unarchived import RotatingFileHandlerUnarchived


class TestRotatingFileHandlerUnarchived:
  """Test the RotatingFileHandlerUnarchived class."""

  def test__initialize__attributes(
      self,
      unarchived_rotating_file_handler_instance: RotatingFileHandlerUnarchived,
      mocked_logger_file_name: str,
  ) -> None:
    assert unarchived_rotating_file_handler_instance.backupCount == 3
    assert unarchived_rotating_file_handler_instance.baseFilename == \
        mocked_logger_file_name
    assert unarchived_rotating_file_handler_instance.encoding == "utf-8"
    # This seems to be broken typing in a distributed stub file.
    assert unarchived_rotating_file_handler_instance.maxBytes == \
        10000000  # type: ignore[comparison-overlap]

  def test__initialize__inheritance(
      self,
      unarchived_rotating_file_handler_instance: RotatingFileHandlerUnarchived,
  ) -> None:
    assert isinstance(
        unarchived_rotating_file_handler_instance,
        logging.handlers.RotatingFileHandler,
    )
