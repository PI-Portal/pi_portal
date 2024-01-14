"""Test the S3UploadCronJobBase class."""

import logging
from io import StringIO
from typing import List
from unittest import mock

from pi_portal.modules.integrations.s3 import client as s3_client
from .. import job, s3_upload_job


class TestS3UploadCronJobBase:
  """Test the S3UploadCronJobBase class."""

  def set_disk_queue(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      files: List[str],
  ) -> None:
    setattr(
        concrete_s3_upload_cron_instance,
        "disk_queue",
        files,
    )

  def test__initialization__attributes(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_disk_queue: mock.Mock,
      mocked_interval: int,
      mocked_cron_logger: logging.Logger,
  ) -> None:
    assert concrete_s3_upload_cron_instance.disk_queue == \
           mocked_disk_queue.return_value
    assert concrete_s3_upload_cron_instance.interval == mocked_interval
    assert concrete_s3_upload_cron_instance.log == mocked_cron_logger
    assert concrete_s3_upload_cron_instance.name == "mock_cron_job"
    assert concrete_s3_upload_cron_instance.path == "mock_path"

  def test__initialization__disk_queue(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_disk_queue: mock.Mock,
  ) -> None:
    mocked_disk_queue.assert_called_once_with(
        concrete_s3_upload_cron_instance.path
    )

  def test__initialization__s3_client(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
  ) -> None:
    assert concrete_s3_upload_cron_instance.s3_client == \
           mocked_s3_client.return_value
    mocked_s3_client.assert_called_once_with()

  def test__initialization__inheritance(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
  ) -> None:
    assert isinstance(
        concrete_s3_upload_cron_instance,
        s3_upload_job.S3UploadCronJobBase,
    )
    assert isinstance(
        concrete_s3_upload_cron_instance,
        job.CronJobBase,
    )

  def test__cron__no_files__calls(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
  ) -> None:
    self.set_disk_queue(concrete_s3_upload_cron_instance, [])

    concrete_s3_upload_cron_instance.cron()

    mocked_s3_client.return_value.upload.assert_not_called()
    mocked_os_remove.assert_not_called()

  def test__cron__no_files__logging(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    self.set_disk_queue(concrete_s3_upload_cron_instance, [])

    concrete_s3_upload_cron_instance.cron()

    assert mocked_cron_logger_stream.getvalue() == ""

  def test__cron__single_file__calls(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
  ) -> None:
    self.set_disk_queue(concrete_s3_upload_cron_instance, ["mock-file1"])

    concrete_s3_upload_cron_instance.cron()

    mocked_s3_client.return_value.upload.assert_called_once_with("mock-file1")
    mocked_os_remove.assert_called_once_with("mock-file1")

  def test__cron__single_file__logging(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    self.set_disk_queue(concrete_s3_upload_cron_instance, ["mock-file1"])
    cron_job_name = concrete_s3_upload_cron_instance.name

    concrete_s3_upload_cron_instance.cron()

    assert mocked_cron_logger_stream.getvalue() == (
        f"INFO - {cron_job_name} - Uploading 'mock-file1' ...\n"
        f"INFO - {cron_job_name} - Removing 'mock-file1' ...\n"
    )

  def test__cron__two_files__calls(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_os_remove: mock.Mock,
      mocked_s3_client: mock.Mock,
  ) -> None:
    self.set_disk_queue(
        concrete_s3_upload_cron_instance, ["mock-file1", "mock-file2"]
    )

    concrete_s3_upload_cron_instance.cron()

    assert mocked_s3_client.return_value.upload.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]
    assert mocked_os_remove.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]

  def test__cron__two_files__logging(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    self.set_disk_queue(
        concrete_s3_upload_cron_instance, ["mock-file1", "mock-file2"]
    )
    cron_job_name = concrete_s3_upload_cron_instance.name

    concrete_s3_upload_cron_instance.cron()

    assert mocked_cron_logger_stream.getvalue() == (
        f"INFO - {cron_job_name} - Uploading 'mock-file1' ...\n"
        f"INFO - {cron_job_name} - Removing 'mock-file1' ...\n"
        f"INFO - {cron_job_name} - Uploading 'mock-file2' ...\n"
        f"INFO - {cron_job_name} - Removing 'mock-file2' ...\n"
    )

  def test__cron__two_files__upload_errors__calls(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
  ) -> None:
    self.set_disk_queue(
        concrete_s3_upload_cron_instance, ["mock-file1", "mock-file2"]
    )
    mocked_s3_client.return_value.upload.side_effect = \
        s3_client.S3BucketException

    concrete_s3_upload_cron_instance.cron()

    assert mocked_s3_client.return_value.upload.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]
    mocked_os_remove.assert_not_called()

  def test__cron__two_files__upload_errors__logging(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    self.set_disk_queue(
        concrete_s3_upload_cron_instance, ["mock-file1", "mock-file2"]
    )
    mocked_s3_client.return_value.upload.side_effect = \
        s3_client.S3BucketException
    cron_job_name = concrete_s3_upload_cron_instance.name

    concrete_s3_upload_cron_instance.cron()

    assert mocked_cron_logger_stream.getvalue() == (
        f"INFO - {cron_job_name} - Uploading 'mock-file1' ...\n"
        f"ERROR - {cron_job_name} - Failed to upload 'mock-file1' ...\n"
        f"INFO - {cron_job_name} - Uploading 'mock-file2' ...\n"
        f"ERROR - {cron_job_name} - Failed to upload 'mock-file2' ...\n"
    )

  def test__cron__two_files__remove_errors__calls(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_s3_client: mock.Mock,
      mocked_os_remove: mock.Mock,
  ) -> None:
    self.set_disk_queue(
        concrete_s3_upload_cron_instance, ["mock-file1", "mock-file2"]
    )
    mocked_os_remove.side_effect = OSError

    concrete_s3_upload_cron_instance.cron()

    assert mocked_s3_client.return_value.upload.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]
    assert mocked_os_remove.mock_calls == [
        mock.call("mock-file1"),
        mock.call("mock-file2"),
    ]

  def test__cron__two_files__remove_errors__logging(
      self,
      concrete_s3_upload_cron_instance: s3_upload_job.S3UploadCronJobBase,
      mocked_os_remove: mock.Mock,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    self.set_disk_queue(
        concrete_s3_upload_cron_instance, ["mock-file1", "mock-file2"]
    )
    mocked_os_remove.side_effect = OSError
    cron_job_name = concrete_s3_upload_cron_instance.name

    concrete_s3_upload_cron_instance.cron()

    assert mocked_cron_logger_stream.getvalue() == (
        f"INFO - {cron_job_name} - Uploading 'mock-file1' ...\n"
        f"INFO - {cron_job_name} - Removing 'mock-file1' ...\n"
        f"ERROR - {cron_job_name} - Failed to remove 'mock-file1' ...\n"
        f"INFO - {cron_job_name} - Uploading 'mock-file2' ...\n"
        f"INFO - {cron_job_name} - Removing 'mock-file2' ...\n"
        f"ERROR - {cron_job_name} - Failed to remove 'mock-file2' ...\n"
    )
