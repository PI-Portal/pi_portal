"""Test the RenderLogIoTemplates class."""

from pi_portal import config
from ...utility.generate_action_render_templates_test import (
    GenericRenderTemplatesActionTest,
)
from .. import action_render_templates


class TestRenderLogIoTemplates(GenericRenderTemplatesActionTest):
  """Test the RenderLogIoTemplates class."""

  action_class = action_render_templates.RenderLogIoTemplates

  def test_initialize__attributes__templates(self) -> None:
    assert len(self.action_class.templates) == 1

  def test_initialize__attributes__filebeat_config(self) -> None:
    filebeat_config = self.action_class.templates[0]
    assert filebeat_config.source == "logzio/filebeat.yml"
    assert filebeat_config.destination == config.PATH_FILEBEAT_CONFIG
    assert filebeat_config.permissions == "600"
    assert filebeat_config.user == config.PI_PORTAL_USER
    assert filebeat_config.group == config.PI_PORTAL_USER
