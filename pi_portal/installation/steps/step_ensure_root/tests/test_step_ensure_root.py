"""Test the StepEnsureRoot class."""

from ...utility.generate_step_test import GenericStepTest
from .. import StepEnsureRoot, action_ensure_root


class TestStepEnsureRoot(GenericStepTest):
  """Test the StepEnsureRoot class."""

  step_class = StepEnsureRoot
  action_classes = [
      action_ensure_root.EnsureRootAction,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Ensuring that the installer is running as root ..."
    )
    assert self.step_class.logging_end_message == (
        "Done ensuring that the installer is running as root."
    )
