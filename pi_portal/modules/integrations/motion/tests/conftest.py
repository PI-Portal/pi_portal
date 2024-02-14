"""Test fixtures for the motion modules tests."""
# pylint: disable=redefined-outer-name

import logging
from unittest import mock

import pytest
from .. import client as motion_client


@pytest.fixture
def mocked_glob() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_http_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_logger() -> logging.Logger:
  logger = logging.getLogger("test")
  return logger


@pytest.fixture
def mocked_os() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def motion_client_instance(
    mocked_glob: mock.Mock,
    mocked_http_client: mock.Mock,
    mocked_logger: logging.Logger,
    mocked_os: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> motion_client.MotionClient:
  monkeypatch.setattr(
      motion_client.__name__ + ".glob.glob",
      mocked_glob,
  )
  monkeypatch.setattr(
      motion_client.__name__ + ".http.HttpClient",
      mocked_http_client,
  )
  monkeypatch.setattr(
      motion_client.__name__ + ".os",
      mocked_os,
  )
  return motion_client.MotionClient(mocked_logger)
