"""Test the SystemCallActionBase class."""
import logging
from unittest import mock

import pytest
from .. import base_action
from ..base_system_call_action import SystemCallActionBase, SystemCallError


class TestSystemCallActionBase:
  """Test the SystemCallActionBase class."""

  def test_initialize__attributes(
      self,
      concrete_action_system_call_base_instance: SystemCallActionBase,
  ) -> None:
    assert isinstance(
        concrete_action_system_call_base_instance.log, logging.Logger
    )

  def test_initialize__inheritance(
      self,
      concrete_action_system_call_base_instance: SystemCallActionBase,
  ) -> None:
    assert isinstance(
        concrete_action_system_call_base_instance,
        base_action.ActionBase,
    )

  def test_system_call__successful__calls_os_system(
      self,
      concrete_action_system_call_base_instance: SystemCallActionBase,
      mocked_os_system: mock.Mock,
  ) -> None:
    mocked_command = "mkdir -p /tmp/pi_portal"
    mocked_os_system.side_effect = [0]

    concrete_action_system_call_base_instance.system_call(mocked_command)

    mocked_os_system.assert_called_once_with(mocked_command)

  def test_system_call__failure__raises_correct_exception(
      self,
      concrete_action_system_call_base_instance: SystemCallActionBase,
      mocked_os_system: mock.Mock,
  ) -> None:
    mocked_command = "mkdir -p /tmp/pi_portal"
    mocked_os_system.side_effect = [127]

    with pytest.raises(SystemCallError):
      concrete_action_system_call_base_instance.system_call(mocked_command)

    mocked_os_system.assert_called_once_with(mocked_command)
