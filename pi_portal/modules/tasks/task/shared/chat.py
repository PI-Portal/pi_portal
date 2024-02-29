"""Shared resources for chat tasks."""

from dataclasses import dataclass

from pi_portal import config
from pi_portal.modules.tasks.task.bases import task_args_base
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)


@dataclass
class ChatUploadTaskArgs(
    ArgFileSystemRestrictionMixin,
    task_args_base.TaskArgsBase,
):
  """Arguments for chat upload tasks."""

  file_system_arg_restrictions = {"path": [config.PATH_CAMERA_CONTENT]}

  description: str
  path: str
