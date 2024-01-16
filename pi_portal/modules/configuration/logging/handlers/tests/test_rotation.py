"""Test the RotatingFileHandlerWithEnqueue class."""

import logging
import logging.handlers
import os
from datetime import datetime, timezone
from unittest import mock

from pi_portal import config
from ..rotation import RotatingFileHandlerWithEnqueue


class TestRotatingFileHandlerWithEnqueue:
  """Test the RotatingFileHandlerWithEnqueue class."""

  base_class_exists_calls = [False, False, False, False]

  def test__initialize__attributes(
      self,
      queuing_rotating_file_handler_instance: RotatingFileHandlerWithEnqueue,
      mocked_logger_file_name: str,
  ) -> None:
    assert queuing_rotating_file_handler_instance.backupCount == 3
    assert queuing_rotating_file_handler_instance.baseFilename == \
        mocked_logger_file_name
    assert queuing_rotating_file_handler_instance.encoding == "utf-8"
    # This seems to be broken typing in a distributed stub file.
    assert queuing_rotating_file_handler_instance.maxBytes == \
        10000000  # type: ignore[comparison-overlap]
    assert queuing_rotating_file_handler_instance.\
        post_rotation_queue_folder == config.PATH_QUEUE_LOG_UPLOAD

  def test__initialize__inheritance(
      self,
      queuing_rotating_file_handler_instance: RotatingFileHandlerWithEnqueue,
  ) -> None:
    assert isinstance(
        queuing_rotating_file_handler_instance,
        logging.handlers.RotatingFileHandler,
    )

  def test__archival_filename__correct_file_path(
      self,
      queuing_rotating_file_handler_instance: RotatingFileHandlerWithEnqueue,
  ) -> None:
    file_name = queuing_rotating_file_handler_instance.archival_filename()

    assert os.path.dirname(file_name) == config.PATH_QUEUE_LOG_UPLOAD

  def test__archival_filename__correct_suffix(
      self,
      queuing_rotating_file_handler_instance: RotatingFileHandlerWithEnqueue,
  ) -> None:
    file_name = queuing_rotating_file_handler_instance.archival_filename()

    assert file_name.endswith(
        os.path.basename(queuing_rotating_file_handler_instance.baseFilename)
    )

  def test__archival_filename__utc_timestamp(
      self,
      queuing_rotating_file_handler_instance: RotatingFileHandlerWithEnqueue,
  ) -> None:

    file_name = queuing_rotating_file_handler_instance.archival_filename()

    assert datetime.fromisoformat(
        os.path.basename(file_name).split("_")[0]
    ).tzinfo == timezone.utc

  def test__log__no_rotation__does_not_enqueue(
      self,
      rotating_logger_instance: logging.Logger,
      mocked_should_rotate: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    mocked_should_rotate.side_effect = [0, 0]

    rotating_logger_instance.info("A")

    mocked_shutil.copy.assert_not_called()

  def test__log__rotation__no_new_file__does_not_enqueue(
      self,
      rotating_logger_instance: logging.Logger,
      mocked_os_path_exists: mock.Mock,
      mocked_should_rotate: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    mocked_should_rotate.side_effect = [1, 0, 0, 0]
    mocked_os_path_exists.side_effect = \
        self.base_class_exists_calls + [False]

    rotating_logger_instance.info("A")

    mocked_shutil.copy.assert_not_called()

  def test__log__rotation__new_file__does_not_secure(
      self,
      rotating_logger_instance: logging.Logger,
      mocked_file_system: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_should_rotate: mock.Mock,
  ) -> None:
    mock_filename = mock.Mock()
    setattr(
        rotating_logger_instance.handlers[0],
        "archival_filename",
        mock_filename,
    )
    mocked_should_rotate.side_effect = [1, 0, 0, 0]
    mocked_os_path_exists.side_effect = \
        self.base_class_exists_calls + [False]

    rotating_logger_instance.info("A")

    mocked_file_system.assert_not_called()

  def test__log__rotation__new_file__enqueues(
      self,
      rotating_logger_instance: logging.Logger,
      mocked_logger_file_name: str,
      mocked_os_path_exists: mock.Mock,
      mocked_should_rotate: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    mock_filename = mock.Mock()
    setattr(
        rotating_logger_instance.handlers[0],
        "archival_filename",
        mock_filename,
    )
    mocked_should_rotate.side_effect = [1, 0, 0, 0]
    mocked_os_path_exists.side_effect = \
        self.base_class_exists_calls + [True]

    rotating_logger_instance.info("A")

    mocked_shutil.copy.assert_called_with(
        mocked_logger_file_name + ".1",
        mock_filename.return_value,
    )

  def test__log__rotation__new_file__is_secured(
      self,
      rotating_logger_instance: logging.Logger,
      mocked_file_system: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_should_rotate: mock.Mock,
  ) -> None:
    mock_filename = mock.Mock()
    setattr(
        rotating_logger_instance.handlers[0],
        "archival_filename",
        mock_filename,
    )
    mocked_should_rotate.side_effect = [1, 0, 0, 0]
    mocked_os_path_exists.side_effect = \
        self.base_class_exists_calls + [True]

    rotating_logger_instance.info("A")

    assert mocked_file_system.mock_calls == [
        mock.call(mock_filename.return_value),
        mock.call().permissions("640")
    ]
