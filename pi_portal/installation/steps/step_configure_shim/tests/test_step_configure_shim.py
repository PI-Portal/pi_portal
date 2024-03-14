"""Test the StepConfigurePiPortalShim class."""

from ...utility.generate_step_test import GenericStepTest
from .. import StepConfigurePiPortalShim, action_render_templates


class TestStepConfigurePiPortalShim(GenericStepTest):
  """Test the StepConfigurePiPortalShim class."""

  step_class = StepConfigurePiPortalShim
  action_classes = [
      action_render_templates.RenderPiPortalShimTemplatesAction,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Configuring the pi_portal shim script ..."
    )
    assert self.step_class.logging_end_message == (
        "Done configuring the pi_portal shim script."
    )
