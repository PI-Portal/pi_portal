"""Test the S3UploadCronJobBase class."""

from typing import List
from unittest import mock

import pytest
from pi_portal.modules.integrations.s3.bases import cron
from pi_portal.modules.mixins import write_log_file
from ... import client
from .conftest import ConcreteS3UploadCronJob


class Interrupt(Exception):
  """Raised to interrupt the cron during testing."""


class TestS3UploadCronJobBase:
  """Test the S3UploadCronJobBase class."""

  logging_upload_prefix = "Uploading '%s' ..."
  logging_remove_prefix = "Removing '%s' ..."
  logging_upload_error_prefix = "Failed to upload '%s' ..."
  logging_remove_error_prefix = "Failed to remove '%s' ..."

  def set_disk_queue(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      files: List[str],
  ) -> None:
    setattr(
        s3_upload_cron_instance,
        "disk_queue",
        files,
    )

  def logging_start_message(
      self,
      mocked_logger: mock.Mock,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
  ) -> None:
    mocked_logger.warning.assert_called_once_with(
        "%s is starting ...",
        s3_upload_cron_instance.__class__.__name__,
    )

  def test__initialization__attrs(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_disk_queue: mock.Mock,
      mocked_interval: int,
      mocked_s3_client: mock.Mock,
  ) -> None:
    assert s3_upload_cron_instance.disk_queue == mocked_disk_queue.return_value
    assert s3_upload_cron_instance.interval == mocked_interval
    assert s3_upload_cron_instance.logger_name == \
           ConcreteS3UploadCronJob.logger_name
    assert s3_upload_cron_instance.log_file_path == \
           ConcreteS3UploadCronJob.log_file_path
    assert isinstance(s3_upload_cron_instance.log, mock.Mock)
    assert s3_upload_cron_instance.path == ConcreteS3UploadCronJob.path
    assert s3_upload_cron_instance.s3_client == mocked_s3_client.return_value

  def test__initialization__composition(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_disk_queue: mock.Mock,
      mocked_s3_client: mock.Mock,
  ) -> None:
    mocked_disk_queue.assert_called_once_with(s3_upload_cron_instance.path)
    mocked_s3_client.assert_called_once_with()

  def test__initialization__inheritance(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
  ) -> None:
    assert isinstance(s3_upload_cron_instance, cron.S3UploadCronJobBase)
    assert isinstance(s3_upload_cron_instance, write_log_file.LogFileWriter)

  def test__start__single_run__no_files__calls(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, [])
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    mocked_s3_client.return_value.upload.assert_not_called()
    mocked_os_remove.assert_not_called()
    mocked_sleep.assert_called_once_with(s3_upload_cron_instance.interval)

  def test__start__single_run__no_files__logging(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_logger: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, [])
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    mocked_logger.warning.assert_called_once_with(
        "%s is starting ...",
        s3_upload_cron_instance.__class__.__name__,
    )
    mocked_logger.info.assert_not_called()
    mocked_logger.error.assert_not_called()

  def test__start__two_runs__no_files__calls(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, [])
    mocked_sleep.side_effect = [None, Interrupt]

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    mocked_s3_client.return_value.upload.assert_not_called()
    mocked_os_remove.assert_not_called()
    assert mocked_sleep.mock_calls == [
        mock.call(s3_upload_cron_instance.interval),
        mock.call(s3_upload_cron_instance.interval),
    ]

  def test__start__two_runs__no_files__logging(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_logger: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, [])
    mocked_sleep.side_effect = [None, Interrupt]

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    self.logging_start_message(
        mocked_logger,
        s3_upload_cron_instance,
    )
    mocked_logger.info.assert_not_called()
    mocked_logger.error.assert_not_called()

  def test__start__single_run__single_file__calls(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1"])
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    mocked_s3_client.return_value.upload.assert_called_once_with("mock-file1",)
    mocked_os_remove.assert_called_once_with("mock-file1",)
    mocked_sleep.assert_called_once_with(s3_upload_cron_instance.interval)

  def test__start__single_run__single_file__logging(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_logger: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1"])
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    self.logging_start_message(
        mocked_logger,
        s3_upload_cron_instance,
    )
    assert mocked_logger.info.mock_calls == [
        mock.call(
            self.logging_upload_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file1",
        ),
    ]
    mocked_logger.error.assert_not_called()

  def test__start__single_run__two_files__calls(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_os_remove: mock.Mock,
      mocked_s3_client: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1", "mock-file2"])
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    assert mocked_s3_client.return_value.upload.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]
    assert mocked_os_remove.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]
    mocked_sleep.assert_called_once_with(s3_upload_cron_instance.interval)

  def test__start__single_run__two_files__logging(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_logger: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1", "mock-file2"])
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    self.logging_start_message(
        mocked_logger,
        s3_upload_cron_instance,
    )
    assert mocked_logger.info.mock_calls == [
        mock.call(
            self.logging_upload_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_upload_prefix,
            "mock-file2",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file2",
        ),
    ]
    mocked_logger.error.assert_not_called()

  def test__start__single_run__two_files__upload_errors__calls(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1", "mock-file2"])
    mocked_s3_client.return_value.upload.side_effect = client.S3BucketException
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    assert mocked_s3_client.return_value.upload.mock_calls == [
        mock.call("mock-file1",),
        mock.call("mock-file2",),
    ]
    mocked_os_remove.assert_not_called()
    mocked_sleep.assert_called_once_with(s3_upload_cron_instance.interval)

  def test__start__single_run__two_files__upload_errors__logging(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_logger: mock.Mock,
      mocked_s3_client: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1", "mock-file2"])
    mocked_s3_client.return_value.upload.side_effect = client.S3BucketException
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    self.logging_start_message(
        mocked_logger,
        s3_upload_cron_instance,
    )
    assert mocked_logger.info.mock_calls == [
        mock.call(
            self.logging_upload_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_upload_prefix,
            "mock-file2",
        ),
    ]
    assert mocked_logger.error.mock_calls == [
        mock.call(
            self.logging_upload_error_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_upload_error_prefix,
            "mock-file2",
        ),
    ]

  def test__start__single_run__two_files__remove_errors__calls(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1", "mock-file2"])
    mocked_os_remove.side_effect = OSError
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    assert mocked_s3_client.return_value.upload.mock_calls == [
        mock.call("mock-file1",),
        mock.call("mock-file2",),
    ]
    assert mocked_os_remove.mock_calls == [
        mock.call("mock-file1",),
        mock.call("mock-file2",),
    ]
    mocked_sleep.assert_called_once_with(s3_upload_cron_instance.interval)

  def test__start__single_run__two_files__remove_errors__logging(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_logger: mock.Mock,
      mocked_os_remove: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1", "mock-file2"])
    mocked_os_remove.side_effect = OSError
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    self.logging_start_message(
        mocked_logger,
        s3_upload_cron_instance,
    )
    assert mocked_logger.info.mock_calls == [
        mock.call(
            self.logging_upload_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_upload_prefix,
            "mock-file2",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file2",
        ),
    ]
    assert mocked_logger.error.mock_calls == [
        mock.call(
            self.logging_remove_error_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_remove_error_prefix,
            "mock-file2",
        ),
    ]

  def test__start__two_runs__two_files__calls(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_os_remove: mock.Mock,
      mocked_s3_client: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1", "mock-file2"])
    mocked_sleep.side_effect = [None, Interrupt]

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    assert mocked_s3_client.return_value.upload.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]
    assert mocked_os_remove.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]
    assert mocked_sleep.mock_calls == [
        mock.call(s3_upload_cron_instance.interval),
        mock.call(s3_upload_cron_instance.interval),
    ]

  def test__start__two_runs__two_files__logging(
      self,
      s3_upload_cron_instance: cron.S3UploadCronJobBase,
      mocked_logger: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    self.set_disk_queue(s3_upload_cron_instance, ["mock-file1", "mock-file2"])
    mocked_sleep.side_effect = [None, Interrupt]

    with pytest.raises(Interrupt):
      s3_upload_cron_instance.start()

    self.logging_start_message(
        mocked_logger,
        s3_upload_cron_instance,
    )
    assert mocked_logger.info.mock_calls == [
        mock.call(
            self.logging_upload_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_upload_prefix,
            "mock-file2",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file2",
        ),
        mock.call(
            self.logging_upload_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file1",
        ),
        mock.call(
            self.logging_upload_prefix,
            "mock-file2",
        ),
        mock.call(
            self.logging_remove_prefix,
            "mock-file2",
        ),
    ]
    mocked_logger.error.assert_not_called()
