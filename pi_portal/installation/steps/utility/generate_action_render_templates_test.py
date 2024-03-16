"""A generic test suite for RenderTemplatesAction subclasses."""

from typing import Type

from pi_portal.installation.actions.action_render_templates import (
    FileSystemTemplate,
    RenderTemplatesAction,
)


class GenericRenderTemplatesActionTest:
  """A generic test suite for RenderTemplatesAction subclasses."""

  action_class: Type[RenderTemplatesAction]

  def test_initialize__templates(self) -> None:
    for template in self.action_class.templates:
      assert isinstance(
          template,
          FileSystemTemplate,
      )

  def test_initialize__inheritance(self) -> None:
    assert issubclass(
        self.action_class,
        RenderTemplatesAction,
    )
