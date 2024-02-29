"""Test MotionClient Integration."""

import logging
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.camera.bases.client import (
    CameraClientBase,
    CameraException,
)
from pi_portal.modules.integrations.camera.motion import client
from pi_portal.modules.integrations.network import http


@pytest.mark.usefixtures("test_state")
class TestMotionClient:
  """Test the MotionClient class."""

  def test_initialization__attributes(
      self,
      motion_client_instance: client.MotionClient,
  ) -> None:
    assert motion_client_instance.snapshot_url == \
        'http://localhost:8080/{0}/action/snapshot'

  def test_initialization__http_client(
      self,
      motion_client_instance: client.MotionClient,
      mocked_http_client: mock.Mock,
      mocked_logger: logging.Logger,
      test_state: state.State,
  ) -> None:
    assert motion_client_instance.http_client == \
        mocked_http_client.return_value
    mocked_http_client.assert_called_once_with(mocked_logger)
    mocked_http_client.return_value.set_basic_auth.assert_called_once_with(
        test_state.user_config["MOTION"]["AUTHENTICATION"]["USERNAME"],
        test_state.user_config["MOTION"]["AUTHENTICATION"]["PASSWORD"],
    )

  def test_initialization__inheritance(
      self,
      motion_client_instance: client.MotionClient,
  ) -> None:
    assert isinstance(
        motion_client_instance,
        client.MotionClient,
    )
    assert isinstance(
        motion_client_instance,
        CameraClientBase,
    )

  @pytest.mark.parametrize("camera_id", [0, 1])
  def test_take_snapshot__vary_camera__success(
      self,
      motion_client_instance: client.MotionClient,
      mocked_http_client: mock.Mock,
      camera_id: int,
  ) -> None:
    motion_client_instance.take_snapshot(camera_id)

    mocked_http_client.return_value.get.assert_called_once_with(
        motion_client_instance.snapshot_url.format(camera_id)
    )

  @pytest.mark.parametrize("camera_id", [0, 1])
  def test_take_snapshot__vary_camera__failure(
      self,
      motion_client_instance: client.MotionClient,
      mocked_http_client: mock.Mock,
      camera_id: int,
  ) -> None:
    mocked_http_client.return_value.get.side_effect = http.HttpClientError

    with pytest.raises(CameraException):
      motion_client_instance.take_snapshot(camera_id)

    mocked_http_client.return_value.get.assert_called_once_with(
        motion_client_instance.snapshot_url.format(camera_id)
    )
