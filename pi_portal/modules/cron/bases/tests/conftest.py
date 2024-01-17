"""Test fixtures for the cron job baseclass tests."""
# pylint: disable=redefined-outer-name

from typing import Type
from unittest import mock

import pytest
from .. import job, s3_upload_job


@pytest.fixture
def mocked_bucket_name() -> str:
  return "mocked_bucket_name"


@pytest.fixture
def mocked_disk_queue() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_interval() -> float:
  return 1


@pytest.fixture
def mocked_os_remove() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_s3_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_sleep() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_cron_instance(
    mocked_interval: int,
    mocked_cron_logger: mock.Mock,
    mocked_sleep: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> job.CronJobBase:

  class ConcreteCronJob(job.CronJobBase):

    name = "mock_cron_job"
    interval = mocked_interval
    path = "mock_path"

    def cron(self) -> None:
      self.log.info("Cron method has been called.", extra={"job": self.name})

  monkeypatch.setattr(
      job.__name__ + ".time.sleep",
      mocked_sleep,
  )
  s3_client = ConcreteCronJob(mocked_cron_logger)
  return s3_client


@pytest.fixture
def concrete_s3_upload_cron_class(
    mocked_bucket_name: str,
    mocked_interval: int,
) -> Type[s3_upload_job.S3UploadCronJobBase]:

  class ConcreteS3UploadCronJob(s3_upload_job.S3UploadCronJobBase):
    bucket_name = mocked_bucket_name
    interval = mocked_interval
    name = "mock_cron_job"
    path = "mock_path"

  return ConcreteS3UploadCronJob


@pytest.fixture
def concrete_s3_upload_cron_instance(
    concrete_s3_upload_cron_class: Type[s3_upload_job.S3UploadCronJobBase],
    mocked_cron_logger: mock.Mock,
    mocked_disk_queue: mock.Mock,
    mocked_os_remove: mock.Mock,
    mocked_s3_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> s3_upload_job.S3UploadCronJobBase:
  monkeypatch.setattr(
      s3_upload_job.__name__ + ".client.S3BucketClient",
      mocked_s3_client,
  )
  monkeypatch.setattr(
      s3_upload_job.__name__ + ".queue.DiskQueueIterator",
      mocked_disk_queue,
  )
  monkeypatch.setattr(
      s3_upload_job.__name__ + ".os.remove",
      mocked_os_remove,
  )
  s3_client = concrete_s3_upload_cron_class(mocked_cron_logger)
  return s3_client
