"""Tests for the ServiceClient class."""

from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.tasks.enums import TaskPriority, TaskType
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
        "priority":
            TaskPriority.EXPRESS.value,
        "on_failure":
            [
                {
                    "type": TaskType.CHAT_UPLOAD_SNAPSHOT.value,
                    "args":
                        {
                            "description":
                                (
                                    task_scheduler_service_client_instance.
                                    deferred_message + description
                                ),
                            "path": path
                        },
                    "priority": TaskPriority.EXPRESS.value,
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
        "priority":
            TaskPriority.EXPRESS.value,
        "on_failure":
            [
                {
                    "type": TaskType.CHAT_UPLOAD_VIDEO.value,
                    "args":
                        {
                            "description":
                                (
                                    task_scheduler_service_client_instance.
                                    deferred_message + description
                                ),
                            "path": path
                        },
                    "priority": TaskPriority.EXPRESS.value,
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
        "priority": TaskPriority.STANDARD.value,
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
