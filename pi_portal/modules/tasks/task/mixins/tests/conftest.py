"""Test fixtures for the processor mixins classes."""
# pylint: disable=redefined-outer-name

from dataclasses import dataclass
from typing import Type

import pytest
from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)


@dataclass
class MockedRestrictedArgs(ArgFileSystemRestrictionMixin, TaskArgsBase):
  file_system_arg_restrictions = {
      "arg1": ["/var/lib", "/var/lib64"],
      "arg2": ["/var/lib", "/var/lib64"]
  }

  arg1: str
  arg2: str


@pytest.fixture
def concrete_fs_args_class() -> Type[MockedRestrictedArgs]:
  return MockedRestrictedArgs


mocked_restricted_paths = [
    path for paths in MockedRestrictedArgs.file_system_arg_restrictions.values()
    for path in paths
]
