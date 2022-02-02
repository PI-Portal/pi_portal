"""User configuration."""

import pathlib
import pprint
from typing import Dict

import pi_portal as root_module
from jsonschema.validators import validator_for
from pi_portal.modules.mixins import json_file


class UserConfigurationException(BaseException):
  """Raised during validation of end user configuration."""


class UserConfiguration(json_file.JSONFileReader):
  """User configuration."""

  validation_schema_path = (
      pathlib.Path(root_module.__file__).parent / "schema" /
      "config_schema.json"
  )

  def __init__(self) -> None:
    self.user_config: Dict[str, str] = {}

  def load(self, file_name: str = "config.json") -> None:
    """Load and validate the end user's configuration file.

    :param file_name: The path to the file to load.
    """

    self.user_config = self.load_json_file(file_name)
    self.validate()

  def validate(self) -> None:
    """Validate the end user's configuration file.

    :raises: :class:`UserConfigurationException`
    """

    schema = self.load_json_file(self.validation_schema_path)

    validator_class = validator_for(schema)
    validator = validator_class(schema)
    errors = []
    for error in validator.iter_errors(self.user_config):
      errors.append(error.message)

    if errors:
      formatted_errors = pprint.pformat(errors)
      raise UserConfigurationException(formatted_errors)
