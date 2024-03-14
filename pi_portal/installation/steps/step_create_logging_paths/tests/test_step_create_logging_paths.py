"""Test the StepCreateLoggingPaths class."""

from ...utility.generate_step_test import GenericStepTest
from .. import StepCreateLoggingPaths, action_create_paths


class TestStepCreateLoggingPaths(GenericStepTest):
  """Test the StepCreateLoggingPaths class."""

  step_class = StepCreateLoggingPaths
  action_classes = [
      action_create_paths.CreateLoggingPathsAction,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Initializing logging paths ..."
    )
    assert self.step_class.logging_end_message == (
        "Done initializing logging paths."
    )
