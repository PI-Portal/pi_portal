"""TemplateFile class."""

import os
from typing import Any, Dict

from jinja2 import Template as JinjaTemplate
from pi_portal import config
from pi_portal.modules.configuration import state


class ConfileFileTemplate:
  """Configuration file template content.

  :param source: The path to the template file.
  :param destination: The path to render the template to.
  """

  def __init__(self, source: str, destination: str) -> None:
    """Initialize a Template instance."""

    self.source = os.path.join(os.path.dirname(__file__), source)
    self.destination = destination
    self.state = state.State()

  def create_context(self) -> Dict[str, Any]:
    """Create a context dictionary for the template.

    :returns: A dictionary of template context variables.
    """

    context = {
        "LOGZ_IO_CODE": self.state.user_config["LOGZ_IO_CODE"],
    }

    for setting in dir(config):
      if not setting.startswith("__"):
        context[setting] = getattr(config, setting)

    return context

  def render(self) -> None:
    """Render the template."""

    with open(self.source, 'r', encoding='utf-8') as file_handle:
      template = JinjaTemplate(source=file_handle.read())

    rendered_template = template.render(self.create_context())

    with open(self.destination, 'w', encoding='utf-8') as file_handle:
      file_handle.write(rendered_template)
