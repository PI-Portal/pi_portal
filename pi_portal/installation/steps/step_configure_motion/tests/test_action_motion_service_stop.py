"""Test the StopMotionServiceAction class."""

from pi_portal.installation.actions.action_manage_service import (
    ServiceOperation,
)
from pi_portal.installation.services.motion import motion_service
from ...utility.generate_action_manage_service_test import (
    GenericManageServiceActionTest,
)
from .. import action_motion_service_stop


class TestStopMotionServiceAction(GenericManageServiceActionTest):
  """Test the StopMotionServiceAction class."""

  action_class = action_motion_service_stop.StopMotionServiceAction
  operation = ServiceOperation.STOP
  service_definition = motion_service
