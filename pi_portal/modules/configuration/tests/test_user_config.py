"""Test the UserConfiguration class."""

import json
import pathlib
from typing import cast
from unittest import mock

import pi_portal
import pytest
from pi_portal.modules.configuration import user_config
from pi_portal.modules.mixins import read_json_file

MOCK_INVALID_JSON = cast(user_config.TypeUserConfig, {"mock_setting": "0123"})
MOCK_VALID_JSON = user_config.TypeUserConfig(
    **{
        "ARCHIVAL":
            {
                "AWS":
                    {
                        "AWS_ACCESS_KEY_ID":
                            "... AWS key with write access ...",
                        "AWS_SECRET_ACCESS_KEY":
                            "... AWS secret key with write access ...",
                        "AWS_S3_BUCKETS":
                            {
                                "LOGS": "... s3 logs bucket name ...",
                                "VIDEOS": "... s3 video bucket name ..."
                            },
                    }
            },
        "CHAT":
            {
                "SLACK":
                    {
                        "SLACK_APP_SIGNING_SECRET":
                            "... secret value from slack ...",
                        "SLACK_APP_TOKEN":
                            "... token from slack ...",
                        "SLACK_BOT_TOKEN":
                            "... token from slack ...",
                        "SLACK_CHANNEL":
                            "... proper name of slack channel ...",
                        "SLACK_CHANNEL_ID":
                            ".. slack's ID for the channel ...",
                    },
            },
        "LOGS": {
            "LOGZ_IO": {
                "LOGZ_IO_TOKEN": "... logz io's logger token ..."
            }
        },
        "SWITCHES":
            {
                "CONTACT_SWITCHES":
                    [
                        {
                            "NAME": "... name and pin-out of a GPIO switch...",
                            "GPIO": 12,
                        },
                    ],
            },
        "TEMPERATURE_SENSORS":
            {
                "DHT11":
                    [
                        {
                            "NAME": "... name and pin-out of a GPIO switch...",
                            "GPIO": 4,
                        }
                    ],
            }
    },
)


class TestUserConfiguration:
  """Test the UserConfiguration class."""

  def test_initialize__attributes(
      self,
      user_configuration_instance: user_config.UserConfiguration,
  ) -> None:
    assert user_configuration_instance.validation_schema_path == (
        pathlib.Path(pi_portal.__file__).parent / "schema" /
        "config_schema.json"
    )

  def test_initialize__inheritance(
      self,
      user_configuration_instance: user_config.UserConfiguration,
  ) -> None:
    assert isinstance(
        user_configuration_instance,
        read_json_file.JSONFileReader,
    )

  def test_load__calls_validate_and_sets_user_config(
      self,
      user_configuration_instance: user_config.UserConfiguration,
  ) -> None:
    with mock.patch(
        user_config.__name__ + ".read_json_file.JSONFileReader.load_json_file",
        mock.Mock(return_value=MOCK_VALID_JSON)
    ):
      with mock.patch.object(
          user_configuration_instance,
          'validate',
      ) as m_validate:

        user_configuration_instance.load()

    assert user_configuration_instance.user_config == \
           MOCK_VALID_JSON
    m_validate.assert_called_once_with()

  def test_validate__valid_configuration(
      self,
      user_configuration_instance: user_config.UserConfiguration,
  ) -> None:
    user_configuration_instance.user_config = MOCK_VALID_JSON

    user_configuration_instance.validate()

  def test_validate__invalid_configuration(
      self,
      user_configuration_instance: user_config.UserConfiguration,
  ) -> None:
    user_configuration_instance.user_config = MOCK_INVALID_JSON
    with pytest.raises(user_config.UserConfigurationException) as exc:

      user_configuration_instance.validate()

    assert json.loads(str(exc.value)) == [
        "'ARCHIVAL' is a required property",
        "'CHAT' is a required property",
        "'LOGS' is a required property",
        "'SWITCHES' is a required property",
        "'TEMPERATURE_SENSORS' is a required property",
    ]
