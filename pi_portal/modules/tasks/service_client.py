"""Client for the task scheduler service."""

import os.path
from datetime import datetime
from typing import Tuple

from pi_portal import config
from pi_portal.modules.system.socket.unix_stream_http_client import (
    UnixStreamHttpClient,
    UnixStreamHttpResponse,
)
from pi_portal.modules.tasks.enums import TaskPriority, TaskType


class TaskSchedulerServiceClient:
  """Client for the task scheduler service."""

  http_client: UnixStreamHttpClient
  deferred_message = "** Deferred! ** "

  def __init__(self) -> None:
    self.http_client = UnixStreamHttpClient(
        config.PI_PORTAL_TASK_MANAGER_SOCKET
    )

  def chat_upload_snapshot(
      self,
      path: str,
  ) -> UnixStreamHttpResponse:
    """Upload camera snapshots to the chat client via the API.

    :param path: The path to the motion snapshot to upload.
    :returns: A response from the task scheduler API.
    """

    camera, video_time = self._parse_motion_file_path(path)
    description = f"Camera: {camera}, Time: {video_time}"

    payload = {
        "type":
            TaskType.CHAT_UPLOAD_SNAPSHOT.value,
        "args": {
            "description": description,
            "path": path
        },
        "priority":
            TaskPriority.EXPRESS.value,
        "on_failure":
            [
                {
                    "type": TaskType.CHAT_UPLOAD_SNAPSHOT.value,
                    "args":
                        {
                            "description": self.deferred_message + description,
                            "path": path
                        },
                    "priority": TaskPriority.EXPRESS.value,
                    "retry_after": 300,
                }
            ]
    }

    return self.http_client.post("/schedule/", payload)

  def chat_upload_video(
      self,
      path: str,
  ) -> UnixStreamHttpResponse:
    """Upload camera videos to the chat client via the API.

    :param path: The path to the motion video to upload.
    :returns: A response from the task scheduler API.
    """

    camera, video_time = self._parse_motion_file_path(path)
    description = f"Motion detected! Camera: {camera}, Time: {video_time}"

    payload = {
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
                            "description": self.deferred_message + description,
                            "path": path,
                        },
                    "priority": TaskPriority.EXPRESS.value,
                    "retry_after": 300,
                }
            ]
    }

    return self.http_client.post("/schedule/", payload)

  def _parse_motion_file_path(self, path: str) -> Tuple[str, str]:
    camera = "Unknown"
    parsed_datetime = "Unknown"
    raw_filename = os.path.basename(path).split(".")[0]

    try:
      camera, raw_datetime = raw_filename.split("-")[0:2]
      parsed_datetime = (
          datetime.strptime(raw_datetime, "%Y%m%d%H%M%S").isoformat()
      )
    except (TypeError, ValueError):
      pass

    return camera, parsed_datetime
