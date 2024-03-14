"""Test the EnsureRootAction class."""
from unittest import mock

import pytest
from .. import action_ensure_root


class TestEnsureRootAction:
  """Test the EnsureRootAction class."""

  def test_initialize__attributes(
      self,
      ensure_root_action_instance: action_ensure_root.EnsureRootAction,
  ) -> None:
    assert ensure_root_action_instance.insufficient_privileges_msg == (
        "The pi_portal configuration installer must be run as root!"
    )

  def test_invoke__is_root__no_exception_raised(
      self,
      ensure_root_action_instance: action_ensure_root.EnsureRootAction,
      mocked_os_geteuid: mock.Mock,
  ) -> None:
    mocked_os_geteuid.return_value = 0

    ensure_root_action_instance.invoke()

  def test_invoke__not_root__raises_correct_exception(
      self,
      ensure_root_action_instance: action_ensure_root.EnsureRootAction,
      mocked_os_geteuid: mock.Mock,
  ) -> None:
    mocked_os_geteuid.return_value = 1000

    with pytest.raises(PermissionError) as exc:
      ensure_root_action_instance.invoke()

    assert str(exc.value
              ) == (ensure_root_action_instance.insufficient_privileges_msg)
