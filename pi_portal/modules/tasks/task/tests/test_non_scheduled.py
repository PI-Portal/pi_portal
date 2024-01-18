"""Test the non_scheduled module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestNonScheduled(GenericTaskModuleTest):
  """Test the non_scheduled module."""

  expected_api_enabled = False
  expected_arg_class = non_scheduled.Args
  expected_return_type = None
  expected_type = enums.TaskType.NON_SCHEDULED
  mock_args = non_scheduled.Args()
  module = non_scheduled
