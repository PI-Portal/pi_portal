"""Test the StepEnableSupervisordService class."""

from ...utility.generate_step_test import GenericStepTest
from .. import (
    StepEnableSupervisordService,
    action_supervisord_service_enable,
    action_supervisord_service_start,
)


class TestStepEnableSupervisordService(GenericStepTest):
  """Test the StepEnableSupervisordService class."""

  step_class = StepEnableSupervisordService
  action_classes = [
      action_supervisord_service_start.StartSupervisordServiceAction,
      action_supervisord_service_enable.EnableSupervisordServiceAction,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Enabling the supervisord service ..."
    )
    assert self.step_class.logging_end_message == (
        "Done enabling the supervisord service."
    )
