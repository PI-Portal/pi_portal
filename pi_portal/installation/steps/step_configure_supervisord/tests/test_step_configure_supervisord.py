"""Test the StepConfigureSupervisord class."""

from ...utility.generate_step_test import GenericStepTest
from .. import (
    StepConfigureSupervisord,
    action_create_paths,
    action_render_templates,
)


class TestStepConfigureSupervisord(GenericStepTest):
  """Test the StepConfigureSupervisord class."""

  step_class = StepConfigureSupervisord
  action_classes = [
      action_create_paths.CreateSupervisordPathsAction,
      action_render_templates.RenderSupervisordTemplatesAction,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Configuring the supervisord service ..."
    )
    assert self.step_class.logging_end_message == (
        "Done configuring the supervisord service."
    )
