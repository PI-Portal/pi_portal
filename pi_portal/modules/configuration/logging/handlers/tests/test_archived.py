"""Test the RotatingFileHandlerArchived class."""

import logging
import logging.handlers
import os
from datetime import datetime, timezone
from unittest import mock

from pi_portal import config
from ..rotation_archived import RotatingFileHandlerArchived


class TestRotatingFileHandlerArchived:
  """Test the RotatingFileHandlerArchived class."""

  base_class_exists_calls = [False, False, False, False]

  def test__initialize__attributes(
      self,
      archived_rotating_file_handler_instance: RotatingFileHandlerArchived,
      mocked_logger_file_name: str,
  ) -> None:
    assert archived_rotating_file_handler_instance.backupCount == 3
    assert archived_rotating_file_handler_instance.baseFilename == \
        mocked_logger_file_name
    assert archived_rotating_file_handler_instance.encoding == "utf-8"
    # This seems to be broken typing in a distributed stub file.
    assert archived_rotating_file_handler_instance.maxBytes == \
        10000000  # type: ignore[comparison-overlap]
    assert archived_rotating_file_handler_instance.\
        post_rotation_queue_folder == config.PATH_QUEUE_LOG_UPLOAD

  def test__initialize__inheritance(
      self,
      archived_rotating_file_handler_instance: RotatingFileHandlerArchived,
  ) -> None:
    assert isinstance(
        archived_rotating_file_handler_instance,
        logging.handlers.RotatingFileHandler,
    )

  def test__archival_filename__correct_file_path(
      self,
      archived_rotating_file_handler_instance: RotatingFileHandlerArchived,
  ) -> None:
    file_name = archived_rotating_file_handler_instance.archival_filename()

    assert os.path.dirname(file_name) == config.PATH_QUEUE_LOG_UPLOAD

  def test__archival_filename__correct_suffix(
      self,
      archived_rotating_file_handler_instance: RotatingFileHandlerArchived,
  ) -> None:
    file_name = archived_rotating_file_handler_instance.archival_filename()

    assert file_name.endswith(
        os.path.basename(archived_rotating_file_handler_instance.baseFilename)
    )

  def test__archival_filename__utc_timestamp(
      self,
      archived_rotating_file_handler_instance: RotatingFileHandlerArchived,
  ) -> None:

    file_name = archived_rotating_file_handler_instance.archival_filename()

    assert datetime.fromisoformat(
        os.path.basename(file_name).split("_")[0]
    ).tzinfo == timezone.utc

  def test__log__no_rotation__does_not_enqueue(
      self,
      archived_logger_instance: logging.Logger,
      mocked_should_rotate: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    mocked_should_rotate.side_effect = [0, 0]

    archived_logger_instance.info("A")

    mocked_shutil.copy.assert_not_called()

  def test__log__rotation__no_new_file__does_not_enqueue(
      self,
      archived_logger_instance: logging.Logger,
      mocked_os_path_exists: mock.Mock,
      mocked_should_rotate: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    mocked_should_rotate.side_effect = [1, 0, 0, 0]
    mocked_os_path_exists.side_effect = \
        self.base_class_exists_calls + [False]

    archived_logger_instance.info("A")

    mocked_shutil.copy.assert_not_called()

  def test__log__rotation__new_file__does_not_secure(
      self,
      archived_logger_instance: logging.Logger,
      mocked_file_system: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_should_rotate: mock.Mock,
  ) -> None:
    mock_filename = mock.Mock()
    setattr(
        archived_logger_instance.handlers[0],
        "archival_filename",
        mock_filename,
    )
    mocked_should_rotate.side_effect = [1, 0, 0, 0]
    mocked_os_path_exists.side_effect = \
        self.base_class_exists_calls + [False]

    archived_logger_instance.info("A")

    mocked_file_system.assert_not_called()

  def test__log__rotation__new_file__enqueues(
      self,
      archived_logger_instance: logging.Logger,
      mocked_logger_file_name: str,
      mocked_os_path_exists: mock.Mock,
      mocked_should_rotate: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    mock_filename = mock.Mock()
    setattr(
        archived_logger_instance.handlers[0],
        "archival_filename",
        mock_filename,
    )
    mocked_should_rotate.side_effect = [1, 0, 0, 0]
    mocked_os_path_exists.side_effect = \
        self.base_class_exists_calls + [True]

    archived_logger_instance.info("A")

    mocked_shutil.copy.assert_called_with(
        mocked_logger_file_name + ".1",
        mock_filename.return_value,
    )

  def test__log__rotation__new_file__is_secured(
      self,
      archived_logger_instance: logging.Logger,
      mocked_file_system: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_should_rotate: mock.Mock,
  ) -> None:
    mock_filename = mock.Mock()
    setattr(
        archived_logger_instance.handlers[0],
        "archival_filename",
        mock_filename,
    )
    mocked_should_rotate.side_effect = [1, 0, 0, 0]
    mocked_os_path_exists.side_effect = \
        self.base_class_exists_calls + [True]

    archived_logger_instance.info("A")

    assert mocked_file_system.mock_calls == [
        mock.call(mock_filename.return_value),
        mock.call().permissions("640")
    ]
