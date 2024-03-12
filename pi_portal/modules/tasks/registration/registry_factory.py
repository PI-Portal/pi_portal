"""Factory to create TaskRegistry instances."""

from typing import Optional

from .registry import TaskRegistry


class RegistryFactory:
  """Factory to create TaskRegistry instances."""

  __slots__ = ()

  cron_job_modules = [
      "archive_logs",
      "archive_videos",
      "manifest_metrics",
      "queue_maintenance",
      "queue_metrics",
      "system_metrics",
  ]
  task_modules = [
      "archive_logs",
      "archive_videos",
      "camera_snapshot",
      "chat_send_message",
      "chat_send_temperature_reading",
      "chat_upload_snapshot",
      "chat_upload_video",
      "file_system_copy",
      "file_system_move",
      "file_system_remove",
      "non_scheduled",
      "queue_maintenance",
  ]
  _registry: Optional[TaskRegistry] = None

  @classmethod
  def create(cls) -> "TaskRegistry":
    """Create a shared task registry instance, loading the required modules.

    :returns: The populated registry.
    """

    if cls._registry:
      return cls._registry

    cls._registry = TaskRegistry()

    for module in cls.task_modules:
      cls._registry.register_task(module)
    for module in cls.cron_job_modules:
      cls._registry.register_cron_job(module)

    return cls._registry
