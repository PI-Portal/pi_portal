"""Test the supervisor_process module."""

from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import supervisor_process
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestSupervisorProcess(GenericTaskModuleTest):
  """Test the supervisor_process module."""

  expected_api_enabled = False
  expected_arg_class = supervisor_process.Args
  expected_return_type = None
  expected_routing_label = enums.RoutingLabel.SUPERVISOR_PROCESS
  expected_type = enums.TaskType.SUPERVISOR_PROCESS
  mock_args = supervisor_process.Args(
      process=ProcessList.CAMERA,
      requested_state=ProcessStatus.STOPPED,
  )
  module = supervisor_process
