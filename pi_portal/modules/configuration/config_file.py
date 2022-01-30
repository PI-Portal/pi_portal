"""User configuration loader."""

import json
import pathlib
import pprint
from typing import Dict

import pi_portal as root_module
from jsonschema.validators import validator_for


class UserConfigurationException(BaseException):
  """Exceptions raised during validation of end user configuration."""


class UserConfiguration:
  """The configuration provided by the end user."""

  def __init__(self):
    self.user_config = {}

  def load(self, file_name: str = "config.json") -> Dict:
    """Load the end user's configuration file.

    :param file_name: The path to the file to load.
    :return: The parsed configuration.
    """

    with open(file_name, "r", encoding="utf-8") as file_handle:
      self.user_config = json.load(file_handle)

    self.validate()

    return self.user_config

  def validate(self):
    """Validate the end user's configuration file."""

    schema_path = pathlib.Path(root_module.__file__).parent / "schema"

    with open(
        schema_path / "config_schema.json", "r", encoding="utf-8"
    ) as file_handle:
      schema = json.load(file_handle)

    validator_class = validator_for(schema)
    validator = validator_class(schema)
    errors = []
    for error in validator.iter_errors(self.user_config):
      errors.append(error.message)

    if errors:
      formatted_errors = pprint.pformat(errors)
      raise UserConfigurationException(formatted_errors)
