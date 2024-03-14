"""A generic test suite for RenderTemplatesAction subclasses."""

import os
from typing import Type

from pi_portal.installation.actions.action_render_templates import (
    RenderTemplatesAction,
)
from pi_portal.installation.templates import config_file


class GenericRenderTemplatesActionTest:
  """A generic test suite for RenderTemplatesAction subclasses."""

  action_class: Type[RenderTemplatesAction]
  templates_base_path = os.path.dirname(config_file.__file__)

  def test_initialize__templates(self) -> None:
    for template in self.action_class.templates:
      assert isinstance(
          template,
          config_file.ConfileFileTemplate,
      )

  def test_initialize__inheritance(self) -> None:
    assert issubclass(
        self.action_class,
        RenderTemplatesAction,
    )
