"""Test the StepCreateDataPaths class."""

from ...utility.generate_step_test import GenericStepTest
from .. import StepCreateDataPaths, action_create_paths


class TestStepCreateDataPaths(GenericStepTest):
  """Test the StepCreateDataPaths class."""

  step_class = StepCreateDataPaths
  action_classes = [
      action_create_paths.CreateDataPathsAction,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Initializing data paths ..."
    )
    assert self.step_class.logging_end_message == (
        "Done initializing data paths."
    )
