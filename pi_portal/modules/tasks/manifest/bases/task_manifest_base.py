"""Task manifest base class."""

import abc
from typing import List, MutableMapping, TypedDict

from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask


class TypeManifestMetrics(TypedDict):
  """Typed representation of a task manifest's metrics."""

  tasks: int


class TaskManifestBase:
  """Base class of a persistent manifest where tasks can be inventoried.

  Implementations must create a persistent dictionary and cache it.
  """

  cached_dict: "MutableMapping[str, TypeGenericTask]"
  persistent_dict: "MutableMapping[str, TypeGenericTask]"

  def __init__(self) -> None:
    self.cached_dict = self._create_cache()

  @abc.abstractmethod
  def _create_cache(self) -> MutableMapping[str, TypeGenericTask]:
    """Create a copy of the persistent dictionary to make a cache."""

  @abc.abstractmethod
  def close(self) -> None:
    """Close any filehandles associated with the persistent dictionary."""

  def add(self, task: "TypeGenericTask") -> None:
    """Add a task to the manifest.

    :param task: The task you wish to add.
    """
    self.persistent_dict[str(task)] = task
    self.cached_dict = self._create_cache()

  @property
  def contents(self) -> "List[TypeGenericTask]":
    """Return the contents of the manifest, without disk activity."""
    return list(self.cached_dict.values())

  def metrics(self) -> "TypeManifestMetrics":
    """Return metrics for this manifest, without disk activity."""
    return TypeManifestMetrics(tasks=len(self.contents))

  def remove(self, task: "TypeGenericTask") -> None:
    """Remove a task from the manifest.

    :param task: The task you wish to add.
    """
    del self.persistent_dict[str(task)]
    self.cached_dict = self._create_cache()
