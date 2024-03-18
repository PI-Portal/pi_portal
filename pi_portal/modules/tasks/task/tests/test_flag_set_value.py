"""Test the flag_set_value module."""
import pytest
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import flag_set_value
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestFlagSetState(GenericTaskModuleTest):
  """Test the flag_set_value module."""

  expected_api_enabled = True
  expected_arg_class = flag_set_value.Args
  expected_return_type = None
  expected_routing_label = enums.RoutingLabel.PI_PORTAL_CONTROL
  expected_type = enums.TaskType.FLAG_SET_VALUE
  mock_args = flag_set_value.Args(
      flag_name="FLAG_CAMERA_DISABLED_BY_CRON",
      value=True,
  )
  module = flag_set_value

  def test_initialize__invalid_flag_type__raises_exception(self) -> None:
    invalid_flag = "NON_EXISTENT_FLAG"

    with pytest.raises(ValueError) as exc:
      flag_set_value.Args(
          flag_name=invalid_flag,
          value=True,
      )

    assert str(exc.value) == f"Invalid flag: '{invalid_flag}' !"
