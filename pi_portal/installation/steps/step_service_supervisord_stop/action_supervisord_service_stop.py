"""StopSupervisordServiceAction class."""

from pi_portal.installation.actions import action_manage_service
from pi_portal.installation.services.supervisor import supervisor_service


class StopSupervisordServiceAction(action_manage_service.ManageServiceAction):
  """Stop the supervisord service."""

  service = supervisor_service
  operation = action_manage_service.ServiceOperation.STOP
