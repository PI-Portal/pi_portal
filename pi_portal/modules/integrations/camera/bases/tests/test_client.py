"""Tests for the CameraClientBase class."""

import logging
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.camera.motion import client


@pytest.mark.usefixtures("test_state")
class TestCameraClientBase:
  """Tests for the CameraClientBase class."""

  def test_initialize__attributes(
      self,
      concrete_camera_client_instance: client.CameraClientBase,
      mocked_camera_logger: logging.Logger,
      test_state: state.State,
  ) -> None:
    assert isinstance(
        concrete_camera_client_instance.current_state,
        state.State,
    )
    assert concrete_camera_client_instance.current_state.user_config == (
        test_state.user_config
    )
    assert concrete_camera_client_instance.log == mocked_camera_logger

  @pytest.mark.parametrize("camera_id", [0, 1])
  def test_take_snapshot__calls_mock_implementation(
      self,
      concrete_camera_client_instance: client.CameraClientBase,
      mocked_camera_implementation: mock.Mock,
      camera_id: int,
  ) -> None:
    concrete_camera_client_instance.take_snapshot(camera_id)

    mocked_camera_implementation.assert_called_once_with(camera_id)
