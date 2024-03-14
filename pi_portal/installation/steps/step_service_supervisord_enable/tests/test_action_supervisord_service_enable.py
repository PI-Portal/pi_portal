"""Test the EnableSupervisordServiceAction class."""

from pi_portal.installation.actions.action_manage_service import (
    ServiceOperation,
)
from pi_portal.installation.services.supervisor import supervisor_service
from ...utility.generate_action_manage_service_test import (
    GenericManageServiceActionTest,
)
from .. import action_supervisord_service_enable


class TestEnableSupervisordServiceAction(GenericManageServiceActionTest):
  """Test the EnableSupervisordServiceAction class."""

  action_class = (
      action_supervisord_service_enable.EnableSupervisordServiceAction
  )
  operation = ServiceOperation.ENABLE
  service_definition = supervisor_service
