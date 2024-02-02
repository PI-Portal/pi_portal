"""Filesystem location restrictions for task arguments."""

import os
from typing import ClassVar, Dict, List


class ArgFileSystemRestrictionMixin:
  """Filesystem location restrictions for task arguments."""

  __slots__ = ()

  file_system_arg_restrictions: ClassVar[Dict[str, List[str]]]

  def __post_init__(self) -> None:
    self.validate_arg_paths()

  def validate_arg_paths(self) -> None:
    """Validate arguments to ensure paths do not violate restrictions."""

    for arg_name, restricted_paths in self.file_system_arg_restrictions.items():
      arg_value = getattr(self, arg_name)
      for restricted_path in restricted_paths:
        if arg_value.startswith(os.path.abspath(restricted_path) + os.sep):
          break
      else:
        raise ValueError(
            f"the location '{arg_value}' specified for the '{arg_name}' "
            "argument cannot be accessed."
        )
