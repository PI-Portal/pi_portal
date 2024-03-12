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
    assert concrete_camera_client_instance.camera_config == (
        test_state.user_config["CAMERA"]
    )
    assert concrete_camera_client_instance.log == mocked_camera_logger

  @pytest.mark.parametrize("low_disk_space", [True, False])
  def test_is_disk_space_available__vary_disk_space__expected_return_value(
      self,
      concrete_camera_client_instance: client.CameraClientBase,
      mocked_shutil: mock.Mock,
      test_state: state.State,
      low_disk_space: bool,
  ) -> None:
    camera_configuration = test_state.user_config["CAMERA"]
    mocked_shutil.disk_usage.return_value.free = (
        camera_configuration["DISK_SPACE_MONITOR"]["THRESHOLD"] * 1000000 +
        (-1 if low_disk_space else 0)
    )

    result = concrete_camera_client_instance.is_disk_space_available()

    assert result is not low_disk_space

  @pytest.mark.parametrize("camera_id", [0, 1])
  def test_take_snapshot__calls_mock_implementation(
      self,
      concrete_camera_client_instance: client.CameraClientBase,
      mocked_camera_implementation: mock.Mock,
      camera_id: int,
  ) -> None:
    concrete_camera_client_instance.take_snapshot(camera_id)

    mocked_camera_implementation.assert_called_once_with(camera_id)
