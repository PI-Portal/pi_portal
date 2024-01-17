"""User configuration."""

import pathlib
import pprint
from typing import cast

import pi_portal as root_module
from jsonschema.validators import validator_for
from pi_portal.modules.mixins import read_json_file
from typing_extensions import TypedDict
from .types.archival_config_type import TypeUserConfigArchival
from .types.chat_config_type import TypeUserConfigChat
from .types.gpio_config_type import (
    TypeUserConfigSwitches,
    TypeUserConfigTemperatureSensors,
)
from .types.logs_config_type import TypeUserConfigLogs


class TypeUserConfig(TypedDict):
  """Typed representation of user configuration."""

  ARCHIVAL: "TypeUserConfigArchival"
  CHAT: "TypeUserConfigChat"
  LOGS: "TypeUserConfigLogs"
  SWITCHES: "TypeUserConfigSwitches"
  TEMPERATURE_SENSORS: "TypeUserConfigTemperatureSensors"


class UserConfigurationException(Exception):
  """Raised during validation of end user configuration."""


class UserConfiguration(read_json_file.JSONFileReader):
  """User configuration."""

  validation_schema_path = (
      pathlib.Path(root_module.__file__).parent / "schema" /
      "config_schema.json"
  )
  user_config: TypeUserConfig

  def load(self, file_path: str = "config.json") -> None:
    """Load and validate the end user's configuration file.

    :param file_path: The path to the file to load.
    """

    self.user_config = cast(TypeUserConfig, self.load_json_file(file_path))
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
