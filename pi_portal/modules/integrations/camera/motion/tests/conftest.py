"""Test fixtures for the motion modules tests."""
# pylint: disable=redefined-outer-name

import logging
from unittest import mock

import pytest
from pi_portal.modules.integrations.camera.motion import client as motion_client


@pytest.fixture
def mocked_http_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_logger() -> logging.Logger:
  logger = logging.getLogger("test")
  return logger


@pytest.fixture
def motion_client_instance(
    mocked_http_client: mock.Mock,
    mocked_logger: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
) -> motion_client.MotionClient:
  monkeypatch.setattr(
      motion_client.__name__ + ".http.HttpClient",
      mocked_http_client,
  )
  return motion_client.MotionClient(mocked_logger)
