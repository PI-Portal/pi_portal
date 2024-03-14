"""Test the RenderPiPortalShimTemplatesAction class."""

import os

from pi_portal import config
from ...utility.generate_action_render_templates_test import (
    GenericRenderTemplatesActionTest,
)
from .. import action_render_templates


class TestRenderPiPortalShimTemplatesAction(GenericRenderTemplatesActionTest):
  """Test the RenderPiPortalShimTemplatesAction class."""

  action_class = action_render_templates.RenderPiPortalShimTemplatesAction

  def test_initialize__attributes__templates(self) -> None:
    assert len(self.action_class.templates) == 1

  def test_initialize__attributes__pi_portal_shim(self) -> None:
    pi_portal_shim = self.action_class.templates[0]
    assert pi_portal_shim.source == os.path.join(
        self.templates_base_path,
        "shim/portal",
    )
    assert pi_portal_shim.destination == config.PI_PORTAL_SHIM
    assert pi_portal_shim.permissions == "755"
    assert pi_portal_shim.user == config.PI_PORTAL_USER
