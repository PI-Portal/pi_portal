"""Test the StepConfigureMotion class."""

from ...utility.generate_step_test import GenericStepTest
from .. import (
    StepConfigureMotion,
    action_create_paths,
    action_motion_service_disable,
    action_motion_service_stop,
    action_render_templates,
)


class TestStepConfigureMotion(GenericStepTest):
  """Test the StepConfigureMotion class."""

  step_class = StepConfigureMotion
  action_classes = [
      action_motion_service_stop.StopMotionServiceAction,
      action_motion_service_disable.DisableMotionServiceAction,
      action_create_paths.CreateMotionPathsAction,
      action_render_templates.RenderMotionTemplatesAction,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Configuring the motion service..."
    )
    assert self.step_class.logging_end_message == (
        "Done configuring the motion service"
    )
