"""Test fixtures for the s3 module's tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import client


@pytest.fixture
def mocked_archival_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_partition_name() -> str:
  return "mocked_partition_name"


@pytest.fixture
def concrete_archival_client_instance(
    mocked_archival_implementation: mock.Mock,
    mocked_partition_name: str,
) -> client.ArchivalClientBase:

  class ConcreteArchivalClient(client.ArchivalClientBase):

    def upload(self, local_file_name: str, archival_file_name: str) -> None:
      mocked_archival_implementation.upload(local_file_name, archival_file_name)

  return ConcreteArchivalClient(mocked_partition_name)
