"""Test the RenderSupervisordTemplatesAction class."""

import os

from pi_portal import config
from ...utility.generate_action_render_templates_test import (
    GenericRenderTemplatesActionTest,
)
from .. import action_render_templates


class TestRenderSupervisordTemplatesAction(GenericRenderTemplatesActionTest):
  """Test the RenderSupervisordTemplatesAction class."""

  action_class = action_render_templates.RenderSupervisordTemplatesAction

  def test_initialize__attributes__templates(self) -> None:
    assert len(self.action_class.templates) == 1

  def test_initialize__attributes__supervisord_config(self) -> None:
    supervisord_config = self.action_class.templates[0]
    assert supervisord_config.source == os.path.join(
        self.templates_base_path,
        "supervisor/supervisord.conf",
    )
    assert supervisord_config.destination == config.PATH_SUPERVISOR_CONFIG
    assert supervisord_config.permissions == "600"
    assert supervisord_config.user == "root"
