"""Test the StopSupervisordServiceAction class."""

from pi_portal.installation.actions import action_manage_service
from pi_portal.installation.services.supervisor import supervisor_service
from ...utility.generate_action_manage_service_test import (
    GenericManageServiceActionTest,
)
from .. import action_supervisord_service_stop


class TestStopSupervisordServiceAction(GenericManageServiceActionTest):
  """Test the StopSupervisordServiceAction class."""

  action_class = action_supervisord_service_stop.StopSupervisordServiceAction
  operation = action_manage_service.ServiceOperation.STOP
  service_definition = supervisor_service
