"""Test Motion Integration."""

import logging
import os
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.integrations.network import http
from .. import client as motion_client


class TestMotion:
  """Test the Motion class."""

  def test_initialization__attributes(
      self,
      motion_client_instance: motion_client.MotionClient,
  ) -> None:
    assert motion_client_instance.snapshot_url == \
        'http://localhost:8080/0/action/snapshot'
    assert motion_client_instance.snapshot_file_name == \
        '/var/lib/motion/lastsnap.jpg'
    assert motion_client_instance.video_glob_pattern == \
        os.path.join(config.PATH_MOTION_CONTENT, '/*.mp4')

  def test_initialization__http_client(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_http_client: mock.Mock,
      mocked_logger: logging.Logger,
  ) -> None:
    assert motion_client_instance.http_client == \
        mocked_http_client.return_value
    mocked_http_client.assert_called_once_with(mocked_logger)

  def test_take_snapshot__success(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_http_client: mock.Mock,
  ) -> None:
    motion_client_instance.take_snapshot()

    mocked_http_client.return_value.get.assert_called_once_with(
        motion_client_instance.snapshot_url
    )

  def test_take_snapshot__failure(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_http_client: mock.Mock,
  ) -> None:
    mocked_http_client.return_value.get.side_effect = http.HttpClientError

    with pytest.raises(motion_client.MotionException):
      motion_client_instance.take_snapshot()

    mocked_http_client.return_value.get.assert_called_once_with(
        motion_client_instance.snapshot_url
    )

  def test_get_latest_video_filename__correct_response(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_glob: mock.Mock,
      mocked_os: mock.Mock,
  ) -> None:
    mocked_glob.return_value = ["1.mp4", "2.mp4"]
    mocked_os.path.getctime.side_effect = [1.01, 1.02]

    file_name = motion_client_instance.get_latest_video_filename()

    assert file_name, mocked_glob.return_value[1]

  def test_cleanup_snapshot__success(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_os: mock.Mock,
  ) -> None:
    mock_snapshot_name = "mock_snapshot.jpg"

    motion_client_instance.cleanup_snapshot(mock_snapshot_name)

    mocked_os.remove.assert_called_once_with(mock_snapshot_name)

  def test_cleanup_snapshot__failure(
      self,
      motion_client_instance: motion_client.MotionClient,
      mocked_os: mock.Mock,
  ) -> None:
    mock_snapshot_name = "mock_snapshot.jpg"
    mocked_os.remove.side_effect = OSError("Boom!")

    with pytest.raises(motion_client.MotionException):
      motion_client_instance.cleanup_snapshot(mock_snapshot_name)

    mocked_os.remove.assert_called_once_with(mock_snapshot_name)
