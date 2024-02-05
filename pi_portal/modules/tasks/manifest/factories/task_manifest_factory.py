"""TaskManifestFactory class."""

import os
from typing import TYPE_CHECKING, Dict

from pi_portal import config
from pi_portal.modules.tasks.manifest.sqlite_dictionary import (
    SqliteDictManifest,
)

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.enums import TaskManifests
  from pi_portal.modules.tasks.manifest.bases.task_manifest_base import (
      TaskManifestBase,
  )


class TaskManifestFactory:
  """Instantiate a task manifest context manager with the selected vendor."""

  vendor_class = SqliteDictManifest
  _manifests: "Dict[TaskManifests, TaskManifestBase]" = {}

  @classmethod
  def create(cls, manifest_name: "TaskManifests") -> "TaskManifestBase":
    """Create the specified manifest, or return an already existing copy.

    :param manifest_name: The name of the manifest database table.
    :returns: The new or existing specified task manifest.
    """

    if manifest_name not in cls._manifests:
      cls._manifests[manifest_name] = cls.vendor_class(
          os.path.join(config.PATH_TASKS_SERVICE_DATABASES, "manifests"),
          manifest_name.value,
      )

    return cls._manifests[manifest_name]
