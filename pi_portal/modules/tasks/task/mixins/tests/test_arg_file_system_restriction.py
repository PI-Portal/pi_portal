"""Test the ArgFileSystemRestrictionMixin class."""
import os
from typing import Type

import pytest
from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)
from .conftest import MockedRestrictedArgs, mocked_restricted_paths


class TestArgFileSystemRestrictionMixin:
  """Test the ArgFileSystemRestrictionMixin class."""

  def test_initialize__attributes(
      self,
      concrete_fs_args_class: Type[MockedRestrictedArgs],
  ) -> None:
    assert concrete_fs_args_class.file_system_arg_restrictions == {
        "arg1": ["/var/lib", "/var/lib64"],
        "arg2": ["/var/lib", "/var/lib64"],
    }

  def test_initialize__inheritance(
      self,
      concrete_fs_args_class: Type[MockedRestrictedArgs],
  ) -> None:
    assert issubclass(
        concrete_fs_args_class,
        TaskArgsBase,
    )
    assert issubclass(
        concrete_fs_args_class,
        ArgFileSystemRestrictionMixin,
    )

  @pytest.mark.parametrize("valid_path", mocked_restricted_paths)
  def test_validate_arg_paths__one_arg_is_a_white_list_folder__exception(
      self,
      concrete_fs_args_class: Type[MockedRestrictedArgs],
      valid_path: str,
  ) -> None:
    valid_file = os.path.join(valid_path, "mock_file.txt")

    with pytest.raises(ValueError) as exc:
      concrete_fs_args_class(arg1=valid_file, arg2=valid_path)

    assert str(exc.value) == (
        f"the location '{valid_path}' specified for the 'arg2' "
        "argument cannot be accessed."
    )

  @pytest.mark.parametrize("valid_path", mocked_restricted_paths)
  def test_validate_arg_paths__both_args_inside_white_list_folder__no_exception(
      self,
      concrete_fs_args_class: Type[MockedRestrictedArgs],
      valid_path: str,
  ) -> None:
    valid_file = os.path.join(valid_path, "mock_file.txt")

    concrete_fs_args_class(arg1=valid_file, arg2=valid_file)

  @pytest.mark.parametrize(
      "invalid_path", ["/", "/root", "/user/home/file.txt"]
  )
  def test_validate_arg_paths__both_args_outside_white_list_folder__exception(
      self,
      concrete_fs_args_class: Type[MockedRestrictedArgs],
      invalid_path: str,
  ) -> None:
    invalid_file = os.path.join(invalid_path, "mock_file.txt")

    with pytest.raises(ValueError) as exc:
      concrete_fs_args_class(arg1=invalid_file, arg2=invalid_file)

    assert str(exc.value) == (
        f"the location '{invalid_file}' specified for the 'arg1' "
        "argument cannot be accessed."
    )

  @pytest.mark.parametrize("valid_path", mocked_restricted_paths)
  def test_validate_arg_paths__both_args_are_a_white_list_folder__exception(
      self,
      concrete_fs_args_class: Type[MockedRestrictedArgs],
      valid_path: str,
  ) -> None:
    with pytest.raises(ValueError) as exc:
      concrete_fs_args_class(arg1=valid_path, arg2=valid_path)

    assert str(exc.value) == (
        f"the location '{valid_path}' specified for the 'arg1' "
        "argument cannot be accessed."
    )
