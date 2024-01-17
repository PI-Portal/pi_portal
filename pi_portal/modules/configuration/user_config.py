"""User configuration."""

import pathlib
import pprint
from typing import List, cast

import pi_portal as root_module
from jsonschema.validators import validator_for
from pi_portal.modules.mixins import read_json_file
from typing_extensions import TypedDict


class TypeUserConfig(TypedDict):
  """Typed representation of user configuration."""

  AWS_ACCESS_KEY_ID: str
  AWS_SECRET_ACCESS_KEY: str
  AWS_S3_BUCKETS: "TypeUserConfigS3Buckets"
  LOGZ_IO_CODE: str
  SLACK_APP_SIGNING_SECRET: str
  SLACK_APP_TOKEN: str
  SLACK_BOT_TOKEN: str
  SLACK_CHANNEL: str
  SLACK_CHANNEL_ID: str
  CONTACT_SWITCHES: List["TypeUserConfigGPIO"]
  TEMPERATURE_SENSORS: "TypeUserConfigTemperatureSensors"


class TypeUserConfigS3Buckets(TypedDict):
  """Typed representation of the required S3 bucket names."""

  LOGS: str
  VIDEOS: str


class TypeUserConfigGPIO(TypedDict):
  """Typed representation of a GPIO connected device."""

  NAME: str
  GPIO: int


class TypeUserConfigTemperatureSensors(TypedDict):
  """Typed representation of GPIO connected temperature sensors."""

  DHT11: List["TypeUserConfigGPIO"]


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
