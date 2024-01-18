"""Shared resources for archive tasks."""

from dataclasses import dataclass

from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase


@dataclass
class ArchivalTaskArgs(TaskArgsBase):
  """Arguments for log archival tasks."""

  archival_path: str
  partition_name: str
