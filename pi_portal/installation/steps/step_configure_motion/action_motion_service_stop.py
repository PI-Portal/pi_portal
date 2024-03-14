"""StopMotionServiceAction classe."""

from pi_portal.installation.actions import action_manage_service
from pi_portal.installation.services.motion import motion_service


class StopMotionServiceAction(action_manage_service.ManageServiceAction):
  """Stop the motion service."""

  service = motion_service
  operation = action_manage_service.ServiceOperation.STOP
