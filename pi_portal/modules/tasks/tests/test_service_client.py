"""Tests for the ServiceClient class."""

from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.tasks.config import DEFERRED_MESSAGE_PREFIX
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.service_client import TaskSchedulerServiceClient


class TestServiceClient:
  """Tests for the ServiceClient class."""

  def test_initialize__unix_stream_http_client(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    assert task_scheduler_service_client_instance.http_client == (
        mocked_unix_stream_http_client.return_value
    )
    mocked_unix_stream_http_client.assert_called_once_with(
        config.PI_PORTAL_TASK_MANAGER_SOCKET
    )

  @pytest.mark.parametrize("camera", [0, 1])
  def test_camera_snapshot__sends_correct_api_request(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
      camera: int,
  ) -> None:
    # pylint: disable=duplicate-code
    expected_payload = {
        "type":
            TaskType.CAMERA_SNAPSHOT.value,
        "args": {
            "camera": camera,
        },
        "on_failure":
            [
                {
                    "type": TaskType.CHAT_SEND_MESSAGE.value,
                    "args":
                        {
                            "message":
                                (
                                    task_scheduler_service_client_instance.
                                    camera_snapshot_failure_message
                                ),
                        },
                    "retry_after": 300,
                }
            ]
    }

    task_scheduler_service_client_instance.camera_snapshot(camera)

    mocked_unix_stream_http_client.return_value.post.assert_called_once_with(
        "/schedule/",
        expected_payload,
    )

  def test_camera_snapshot__returns_expected_response(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    mocked_camera = 1

    response = task_scheduler_service_client_instance.camera_snapshot(
        camera=mocked_camera
    )

    assert response == (
        mocked_unix_stream_http_client.return_value.post.return_value
    )

  @pytest.mark.parametrize("message", ["red!", "blue!"])
  def test_chat_send_message__sends_correct_api_request(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
      message: str,
  ) -> None:
    # pylint: disable=duplicate-code
    expected_payload = {
        "type":
            TaskType.CHAT_SEND_MESSAGE.value,
        "args": {
            "message": message,
        },
        "on_failure":
            [
                {
                    "type": TaskType.CHAT_SEND_MESSAGE.value,
                    "args": {
                        "message": DEFERRED_MESSAGE_PREFIX + message,
                    },
                    "retry_after": 300,
                }
            ]
    }

    task_scheduler_service_client_instance.chat_send_message(message)

    mocked_unix_stream_http_client.return_value.post.assert_called_once_with(
        "/schedule/",
        expected_payload,
    )

  def test_chat_send_message__returns_expected_response(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    mocked_message = "red!"

    response = task_scheduler_service_client_instance.chat_send_message(
        message=mocked_message
    )

    assert response == (
        mocked_unix_stream_http_client.return_value.post.return_value
    )

  def test_chat_send_temperature_reading__sends_correct_api_request(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    # pylint: disable=duplicate-code
    header = "Latest temperature readings:"

    expected_payload = {
        "type":
            TaskType.CHAT_SEND_TEMPERATURE_READING.value,
        "args": {
            "header": header,
        },
        "on_failure":
            [
                {
                    "type": TaskType.CHAT_SEND_TEMPERATURE_READING.value,
                    "args": {
                        "header": DEFERRED_MESSAGE_PREFIX + header,
                    },
                    "retry_after": 300,
                }
            ]
    }

    task_scheduler_service_client_instance.chat_send_temperature_reading()

    mocked_unix_stream_http_client.return_value.post.assert_called_once_with(
        "/schedule/",
        expected_payload,
    )

  def test_chat_send_temperature_reading__returns_expected_response(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    response = (
        task_scheduler_service_client_instance.chat_send_temperature_reading()
    )

    assert response == (
        mocked_unix_stream_http_client.return_value.post.return_value
    )

  @pytest.mark.parametrize(
      "path,description",
      [
          [
              "/var/lib/motion/mocked_filename.jpg",
              "Camera: Unknown, Time: Unknown",
          ],
          [
              "/var/lib/motion/1-mocked_filename.jpg",
              "Camera: 1, Time: Unknown",
          ],
          [
              "/var/lib/motion/1-20241201000102.jpg",
              "Camera: 1, Time: 2024-12-01T00:01:02",
          ],
      ],
  )
  def test_chat_upload_snapshot__sends_correct_api_request(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
      path: str,
      description: str,
  ) -> None:
    # pylint: disable=duplicate-code
    expected_payload = {
        "type":
            TaskType.CHAT_UPLOAD_SNAPSHOT.value,
        "args": {
            "description": description,
            "path": path,
        },
        "on_failure":
            [
                {
                    "type": TaskType.CHAT_UPLOAD_SNAPSHOT.value,
                    "args":
                        {
                            "description":
                                DEFERRED_MESSAGE_PREFIX + description,
                            "path":
                                path
                        },
                    "retry_after": 300,
                }
            ]
    }

    task_scheduler_service_client_instance.chat_upload_snapshot(path)

    mocked_unix_stream_http_client.return_value.post.assert_called_once_with(
        "/schedule/",
        expected_payload,
    )

  def test_chat_upload_snapshot__returns_expected_response(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    mocked_path = "/var/lib/motion/mocked_filename.jpg"

    response = task_scheduler_service_client_instance.chat_upload_snapshot(
        mocked_path
    )

    assert response == (
        mocked_unix_stream_http_client.return_value.post.return_value
    )

  @pytest.mark.parametrize(
      "path,description",
      [
          [
              "/var/lib/motion/mocked_filename.mp4",
              "Motion detected! Camera: Unknown, Time: Unknown",
          ],
          [
              "/var/lib/motion/1-mocked_filename.mp4",
              "Motion detected! Camera: 1, Time: Unknown",
          ],
          [
              "/var/lib/motion/1-20241201000102.mp4",
              "Motion detected! Camera: 1, Time: 2024-12-01T00:01:02",
          ],
      ],
  )
  def test_chat_upload_video__sends_correct_api_request(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
      path: str,
      description: str,
  ) -> None:
    # pylint: disable=duplicate-code
    expected_payload = {
        "type":
            TaskType.CHAT_UPLOAD_VIDEO.value,
        "args": {
            "description": description,
            "path": path,
        },
        "on_failure":
            [
                {
                    "type": TaskType.CHAT_UPLOAD_VIDEO.value,
                    "args":
                        {
                            "description":
                                DEFERRED_MESSAGE_PREFIX + description,
                            "path":
                                path
                        },
                    "retry_after": 300,
                }
            ]
    }

    task_scheduler_service_client_instance.chat_upload_video(path)

    mocked_unix_stream_http_client.return_value.post.assert_called_once_with(
        "/schedule/",
        expected_payload,
    )

  def test_chat_upload_video__returns_expected_response(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    mocked_path = "/var/lib/motion/mocked_filename.mp4"

    response = task_scheduler_service_client_instance.chat_upload_video(
        mocked_path
    )

    assert response == (
        mocked_unix_stream_http_client.return_value.post.return_value
    )

  def test_file_system_copy__sends_correct_api_request(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    mocked_destination = "/var/folder2/mocked_filename"
    mocked_source = "/var/folder1/mocked_filename"
    # pylint: disable=duplicate-code
    expected_payload = {
        "type": TaskType.FILE_SYSTEM_COPY.value,
        "args": {
            "destination": mocked_destination,
            "source": mocked_source
        },
    }

    task_scheduler_service_client_instance.file_system_copy(
        mocked_source,
        mocked_destination,
    )

    mocked_unix_stream_http_client.return_value.post.assert_called_once_with(
        "/schedule/",
        expected_payload,
    )

  def test_file_system_copy__returns_expected_response(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    mocked_destination = "/var/folder2/mocked_filename"
    mocked_source = "/var/folder1/mocked_filename"

    response = task_scheduler_service_client_instance.file_system_copy(
        mocked_source,
        mocked_destination,
    )

    assert response == (
        mocked_unix_stream_http_client.return_value.post.return_value
    )

  def test_set_flag__sends_correct_api_request(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    mocked_flag_name = "mocked_flag_name"
    mocked_value = False
    # pylint: disable=duplicate-code
    expected_payload = {
        "type": TaskType.FLAG_SET_VALUE.value,
        "args": {
            "flag_name": mocked_flag_name,
            "value": mocked_value
        },
    }

    task_scheduler_service_client_instance.set_flag(
        mocked_flag_name,
        mocked_value,
    )

    mocked_unix_stream_http_client.return_value.post.assert_called_once_with(
        "/schedule/",
        expected_payload,
    )

  def test_set_flag__returns_expected_response(
      self,
      task_scheduler_service_client_instance: TaskSchedulerServiceClient,
      mocked_unix_stream_http_client: mock.Mock,
  ) -> None:
    mocked_flag_name = "mocked_flag_name"
    mocked_value = False

    response = task_scheduler_service_client_instance.set_flag(
        mocked_flag_name,
        mocked_value,
    )

    assert response == (
        mocked_unix_stream_http_client.return_value.post.return_value
    )
