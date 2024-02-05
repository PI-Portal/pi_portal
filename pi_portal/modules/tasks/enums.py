"""Enums for the task scheduler module."""

import enum


class TaskType(enum.Enum):
  """Pi Portal schedulable task types."""

  BASE = "BASE"
  ARCHIVE_LOGS = "ARCHIVE_LOGS"
  ARCHIVE_VIDEOS = "ARCHIVE_VIDEOS"
  CHAT_SEND_MESSAGE = "CHAT_SEND_MESSAGE"
  CHAT_UPLOAD_SNAPSHOT = "CHAT_UPLOAD_SNAPSHOT"
  CHAT_UPLOAD_VIDEO = "CHAT_UPLOAD_VIDEO"
  FILE_SYSTEM_MOVE = "FILE_SYSTEM_MOVE"
  FILE_SYSTEM_REMOVE = "FILE_SYSTEM_REMOVE"
  MOTION_SNAPSHOT = "MOTION_SNAPSHOT"
  NON_SCHEDULED = "NON_SCHEDULED"
  QUEUE_MAINTENANCE = "QUEUE_MAINTENANCE"


class TaskPriority(enum.Enum):
  """Priorities for task routing."""

  EXPRESS = "EXPRESS"
  STANDARD = "STANDARD"


class TaskManifests(enum.Enum):
  """Manifests for task inventorying."""

  FAILED_TASKS = "FAILED_TASKS"
