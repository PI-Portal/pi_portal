"""Test fixtures for the s3 module's tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.s3.bases import cron

CRON_MODULE = cron.__name__


@pytest.fixture
def mocked_disk_queue() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_interval() -> float:
  return 1


@pytest.fixture
def mocked_logger() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_remove() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_s3_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_sleep() -> mock.Mock:
  return mock.Mock()


class ConcreteS3UploadCronJob(cron.S3UploadCronJobBase):
  log_file_path = "/var/log/mock.log"
  logger_name = "mock_logger"
  path = "mock_path"


@pytest.fixture
def s3_upload_cron_instance(
    # pylint: disable=too-many-arguments
    mocked_disk_queue: mock.Mock,
    mocked_interval: int,
    mocked_logger: mock.Mock,
    mocked_os_remove: mock.Mock,
    mocked_s3_client: mock.Mock,
    mocked_sleep: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> cron.S3UploadCronJobBase:
  with mock_state.mock_state_creator():
    monkeypatch.setattr(
        CRON_MODULE + ".client.S3BucketClient", mocked_s3_client
    )
    monkeypatch.setattr(
        CRON_MODULE + ".queue.DiskQueueIterator", mocked_disk_queue
    )
    monkeypatch.setattr(CRON_MODULE + ".os.remove", mocked_os_remove)
    monkeypatch.setattr(CRON_MODULE + ".time.sleep", mocked_sleep)
    s3_client = ConcreteS3UploadCronJob(mocked_interval)
    s3_client.log = mocked_logger
  return s3_client
