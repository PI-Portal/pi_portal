"""Test the camera_snapshot module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import camera_snapshot
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestCameraSnapshot(GenericTaskModuleTest):
  """Test the camera_snapshot module."""

  expected_api_enabled = True
  expected_arg_class = camera_snapshot.Args
  expected_return_type = None
  expected_routing_label = enums.RoutingLabel.CAMERA
  expected_type = enums.TaskType.CAMERA_SNAPSHOT
  mock_args = camera_snapshot.Args(camera=2)
  module = camera_snapshot
