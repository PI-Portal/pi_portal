"""Test Motion Integration."""

import logging
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.network import http
from .. import client as motion_client


@pytest.mark.usefixtures("test_state")
class TestMotion:
  """Test the Motion class."""

  def test_initialization__attributes(
      self,
      motion_client_instance: motion_client.MotionClient,
  ) -> None:
    assert motion_client_instance.snapshot_url == \
        'http://localhost:8080/{0}/action/snapshot'

  def test_initialization__http_client(
      self,
      motion_client_instance: motion_client.MotionClient,
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

  def test_take_snapshot__default_camera__success(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_http_client: mock.Mock,
  ) -> None:
    motion_client_instance.take_snapshot()

    mocked_http_client.return_value.get.assert_called_once_with(
        motion_client_instance.snapshot_url.format(0)
    )

  def test_take_snapshot__specific_camera__success(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_http_client: mock.Mock,
  ) -> None:
    motion_client_instance.take_snapshot(2)

    mocked_http_client.return_value.get.assert_called_once_with(
        motion_client_instance.snapshot_url.format(2)
    )

  def test_take_snapshot__default_camera__failure(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_http_client: mock.Mock,
  ) -> None:
    mocked_http_client.return_value.get.side_effect = http.HttpClientError

    with pytest.raises(motion_client.MotionException):
      motion_client_instance.take_snapshot()

    mocked_http_client.return_value.get.assert_called_once_with(
        motion_client_instance.snapshot_url.format(0)
    )
