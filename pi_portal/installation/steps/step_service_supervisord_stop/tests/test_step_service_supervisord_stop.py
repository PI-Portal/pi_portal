"""Test the StepStopSupervisordService class."""

from ...utility.generate_step_test import GenericStepTest
from .. import StepStopSupervisordService, action_supervisord_service_stop


class TestStepStopSupervisordService(GenericStepTest):
  """Test the StepStopSupervisordService class."""

  step_class = StepStopSupervisordService
  action_classes = [
      action_supervisord_service_stop.StopSupervisordServiceAction,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Stopping the supervisord service ..."
    )
    assert self.step_class.logging_end_message == (
        "Done stopping the supervisord service."
    )
