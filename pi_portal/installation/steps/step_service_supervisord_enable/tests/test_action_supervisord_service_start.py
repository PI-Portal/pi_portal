"""Test the StartSupervisordServiceAction class."""

from pi_portal.installation.actions.action_manage_service import (
    ServiceOperation,
)
from pi_portal.installation.services.supervisor import supervisor_service
from ...utility.generate_action_manage_service_test import (
    GenericManageServiceActionTest,
)
from .. import action_supervisord_service_start


class TestStartSupervisordServiceAction(GenericManageServiceActionTest):
  """Test the StartSupervisordServiceAction class."""

  action_class = (
      action_supervisord_service_start.StartSupervisordServiceAction
  )
  operation = ServiceOperation.START
  service_definition = supervisor_service
