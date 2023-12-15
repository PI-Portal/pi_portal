#!/usr/bin/python

import argparse
import os
from typing import Any, Dict

import yaml
from jinja2 import Template as JinjaTemplate


def generate(architecture_file: str) -> None:
  """Generate the docker-compose file for these architectures."""

  context: Dict[str, Any] = dict(services={})

  template_file = os.path.join(
      os.path.dirname(architecture_file),
      "docker-compose.yml.j2",
  )

  with open(architecture_file, 'r', encoding='utf-8') as file_handle:
    context["services"] = yaml.safe_load(file_handle)

  with open(template_file, 'r', encoding='utf-8') as file_handle:
    template = JinjaTemplate(source=file_handle.read())

  print(template.render(context))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "architecture_file",
      help="the path to the architecture definition file",
  )
  args = parser.parse_args()
  generate(args.architecture_file)
