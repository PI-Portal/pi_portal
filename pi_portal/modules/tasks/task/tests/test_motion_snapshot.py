"""Test the motion_snapshot module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import motion_snapshot
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestMotionSnapshot(GenericTaskModuleTest):
  """Test the motion_snapshot module."""

  expected_api_enabled = True
  expected_arg_class = motion_snapshot.Args
  expected_return_type = None
  expected_routing_label = enums.RoutingLabel.CAMERA
  expected_type = enums.TaskType.MOTION_SNAPSHOT
  mock_args = motion_snapshot.Args(camera=2)
  module = motion_snapshot
