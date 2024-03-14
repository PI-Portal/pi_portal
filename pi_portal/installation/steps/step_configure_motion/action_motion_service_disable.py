"""DisableMotionServiceAction class."""

from pi_portal.installation.actions import action_manage_service
from pi_portal.installation.services.motion import motion_service


class DisableMotionServiceAction(action_manage_service.ManageServiceAction):
  """Disable the motion service."""

  service = motion_service
  operation = action_manage_service.ServiceOperation.DISABLE
