"""EnableSupervisordServiceAction class."""

from pi_portal.installation.actions import action_manage_service
from pi_portal.installation.services.supervisor import supervisor_service


class EnableSupervisordServiceAction(action_manage_service.ManageServiceAction):
  """Enable the supervisord service."""

  service = supervisor_service
  operation = action_manage_service.ServiceOperation.ENABLE
