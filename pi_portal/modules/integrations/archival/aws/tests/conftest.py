"""Test fixtures for the s3 module's tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from pi_portal.modules.integrations.archival.aws import client


@pytest.fixture
def mocked_boto() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_bucket_name() -> str:
  return "mocked_bucket_name"


@pytest.fixture
def aws_archival_client_instance(
    mocked_boto: mock.Mock,
    mocked_bucket_name: str,
    monkeypatch: pytest.MonkeyPatch,
) -> client.S3BucketClient:
  monkeypatch.setattr(
      client.__name__ + ".boto3",
      mocked_boto,
  )
  return client.S3BucketClient(mocked_bucket_name)
