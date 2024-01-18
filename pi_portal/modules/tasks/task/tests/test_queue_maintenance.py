"""Test the queue_maintenance module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import queue_maintenance
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestQueueMaintenance(GenericTaskModuleTest):
  """Test the queue_maintenance module."""

  expected_api_enabled = False
  expected_arg_class = queue_maintenance.Args
  expected_return_type = None
  expected_type = enums.TaskType.QUEUE_MAINTENANCE
  mock_args = queue_maintenance.Args()
  module = queue_maintenance
