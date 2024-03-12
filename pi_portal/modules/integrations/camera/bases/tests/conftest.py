"""Test fixtures for the camera integration bases modules tests."""
# pylint: disable=redefined-outer-name

import logging
from typing import Type
from unittest import mock

import pytest
from pi_portal.modules.integrations.camera.bases import client


@pytest.fixture
def mocked_camera_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_camera_client_class(
    mocked_camera_implementation: mock.Mock, mocked_shutil: mock.Mock,
    monkeypatch: pytest.MonkeyPatch
) -> Type[client.CameraClientBase]:

  class ConcreteCameraClient(client.CameraClientBase):

    def take_snapshot(self, camera: int) -> None:
      mocked_camera_implementation(camera)

  monkeypatch.setattr(
      client.__name__ + ".shutil",
      mocked_shutil,
  )

  return ConcreteCameraClient


@pytest.fixture
def concrete_camera_client_instance(
    concrete_camera_client_class: Type[client.CameraClientBase],
    mocked_camera_logger: logging.Logger,
) -> client.CameraClientBase:
  return concrete_camera_client_class(mocked_camera_logger)
