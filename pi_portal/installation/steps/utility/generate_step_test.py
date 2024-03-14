"""A generic test suite for StepBase subclasses."""

from typing import List, Type

from pi_portal.installation.actions.bases.base_action import ActionBase
from pi_portal.installation.steps.bases.base_step import StepBase


class GenericStepTest:
  """A generic test suite for StepBase subclasses."""

  step_class: Type[StepBase]
  action_classes: List[Type[ActionBase]]

  def test_initialize__attributes__logging(self) -> None:
    assert isinstance(self.step_class.logging_begin_message, str)
    assert isinstance(self.step_class.logging_end_message, str)

  def test_initialize__actions(self) -> None:
    assert self.step_class.actions == self.action_classes
    for action in self.step_class.actions:
      assert action in self.action_classes
      assert issubclass(
          action,
          ActionBase,
      )

  def test_initialize__inheritance(self) -> None:
    assert issubclass(
        self.step_class,
        StepBase,
    )
