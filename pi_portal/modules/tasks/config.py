"""Configuration for the task scheduler service."""

from collections import defaultdict
from typing import DefaultDict, Dict

from .enums import RoutingLabel, TaskType

QUEUE_WORKER_CONFIGURATION: Dict[RoutingLabel, int] = {
    RoutingLabel.ARCHIVAL: 1,
    RoutingLabel.CAMERA: 1,
    RoutingLabel.CHAT_SEND_MESSAGE: 1,
    RoutingLabel.CHAT_UPLOAD_SNAPSHOT: 1,
    RoutingLabel.CHAT_UPLOAD_VIDEO: 2,
    RoutingLabel.FILE_SYSTEM: 1,
    RoutingLabel.PI_PORTAL_CONTROL: 1
}

ROUTING_MATRIX: DefaultDict[TaskType, RoutingLabel] = defaultdict(
    lambda: RoutingLabel.PI_PORTAL_CONTROL, {
        TaskType.ARCHIVE_LOGS: RoutingLabel.ARCHIVAL,
        TaskType.ARCHIVE_VIDEOS: RoutingLabel.ARCHIVAL,
        TaskType.CAMERA_SNAPSHOT: RoutingLabel.CAMERA,
        TaskType.CHAT_SEND_MESSAGE: RoutingLabel.CHAT_SEND_MESSAGE,
        TaskType.CHAT_UPLOAD_SNAPSHOT: RoutingLabel.CHAT_UPLOAD_SNAPSHOT,
        TaskType.CHAT_UPLOAD_VIDEO: RoutingLabel.CHAT_UPLOAD_VIDEO,
        TaskType.FILE_SYSTEM_COPY: RoutingLabel.FILE_SYSTEM,
        TaskType.FILE_SYSTEM_MOVE: RoutingLabel.FILE_SYSTEM,
        TaskType.FILE_SYSTEM_REMOVE: RoutingLabel.FILE_SYSTEM,
    }
)
