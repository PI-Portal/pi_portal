"""A generic test suite for ManageServiceAction subclasses."""

from typing import Type

from pi_portal.installation.actions.action_manage_service import (
    ManageServiceAction,
    ServiceOperation,
)
from pi_portal.installation.services.bases.service_definition import (
    ServiceDefinition,
)


class GenericManageServiceActionTest:
  """A generic test suite for ManageServiceAction subclasses."""

  action_class: Type[ManageServiceAction]
  operation: ServiceOperation
  service_definition: ServiceDefinition

  def test_initialize__service_operation(self) -> None:
    assert self.action_class.operation == self.operation
    assert isinstance(
        self.action_class.operation,
        ServiceOperation,
    )

  def test_initialize__service_definition(self) -> None:
    assert self.action_class.service == self.service_definition
    assert isinstance(
        self.action_class.service,
        ServiceDefinition,
    )

  def test_initialize__inheritance(self) -> None:
    assert issubclass(
        self.action_class,
        ManageServiceAction,
    )
