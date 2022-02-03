"""Test the UserConfiguration class."""

import json
from unittest import TestCase, mock

from pi_portal.modules.configuration import user_config
from pi_portal.modules.mixins import json_file

MOCK_CONFIG = '{"mock_setting": true}'
MOCK_JSON = {
    "mock_setting": "0123"
}
MOCK_VALID_JSON = {
    "AWS_ACCESS_KEY_ID":
        "... AWS key with write access to video bucket ...",
    "AWS_SECRET_ACCESS_KEY":
        "... AWS secret key with write access to video bucket ...",
    "S3_BUCKET_NAME":
        "... s3 video bucket name ...",
    "LOGZ_IO_CODE":
        "... logz io's logger code ...",
    "SLACK_BOT_TOKEN":
        "...token from slack...",
    "SLACK_CHANNEL":
        "... proper name of slack channel ...",
    "SLACK_CHANNEL_ID":
        ".. slack's ID for the channel ...",
}


class TestUserConfigurationLoad(TestCase):
  """Test the UserConfiguration class load method."""

  def setUp(self) -> None:
    self.configuration = user_config.UserConfiguration()

  def test_initialization(self) -> None:
    config = user_config.UserConfiguration()
    self.assertEqual(config.user_config, {})

  @mock.patch(
      json_file.__name__ + ".JSONFileReader.load_json_file",
      return_value=MOCK_JSON
  )
  def test_load(self, _: mock.Mock) -> None:
    with mock.patch.object(self.configuration, 'validate') as m_validate:
      self.configuration.load()
      self.assertEqual(self.configuration.user_config, MOCK_JSON)
      m_validate.assert_called_once_with()


class TestUserConfigurationValidate(TestCase):
  """Test the UserConfiguration class validate method."""

  def setUp(self) -> None:
    self.configuration = user_config.UserConfiguration()

  def test_valid(self) -> None:
    self.configuration.user_config = MOCK_VALID_JSON
    self.configuration.validate()

  def test_invalid(self) -> None:
    self.configuration.user_config = MOCK_JSON

    with self.assertRaises(user_config.UserConfigurationException) as exc:
      self.configuration.validate()

    self.assertListEqual(
        json.loads(exc.exception.args[0]), [
            "'AWS_ACCESS_KEY_ID' is a required property",
            "'AWS_SECRET_ACCESS_KEY' is a required property",
            "'LOGZ_IO_CODE' is a required property",
            "'S3_BUCKET_NAME' is a required property",
            "'SLACK_BOT_TOKEN' is a required property",
            "'SLACK_CHANNEL' is a required property",
            "'SLACK_CHANNEL_ID' is a required property",
        ]
    )