"""Test fixtures for the s3 module's tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from pi_portal.modules.integrations.s3 import client

CLIENT_MODULE = client.__name__


@pytest.fixture
def mocked_boto() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_bucket_name() -> str:
  return "mocked_bucket_name"


@pytest.fixture
def s3_client_instance(
    mocked_boto: mock.Mock,
    mocked_bucket_name: str,
    monkeypatch: pytest.MonkeyPatch,
) -> client.S3BucketClient:
  monkeypatch.setattr(CLIENT_MODULE + ".boto3", mocked_boto)
  return client.S3BucketClient(mocked_bucket_name)
