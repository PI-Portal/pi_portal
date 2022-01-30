"""Test user configuration loader."""

import json
from unittest import TestCase, mock

from pi_portal.modules.configuration import config_file

MOCK_CONFIG = '{"mock_setting": true}'
MOCK_JSON = {
    "mock_setting": True
}
MOCK_VALID_JSON = {
    "AWS_ACCESS_KEY_ID": "... AWS key with write access to video bucket ...",
    "AWS_SECRET_ACCESS_KEY":
        ("... AWS secret key with write access to video bucket ..."),
    "S3_BUCKET_NAME": "... s3 video bucket name ...",
    "LOGZ_IO_CODE": "... logz io's logger code ...",
    "SLACK_BOT_TOKEN": "...token from slack...",
    "SLACK_CHANNEL": "... proper name of slack channel ...",
    "SLACK_CHANNEL_ID": ".. slack's ID for the channel ...",
}


class TestUserConfigurationLoad(TestCase):
  """Test the UserConfiguration class load method."""

  def setUp(self):
    self.configuration = config_file.UserConfiguration()

  def test_initialization(self):
    config = config_file.UserConfiguration()
    self.assertEqual(config.user_config, {})

  @mock.patch(
      config_file.__name__ + ".open", mock.mock_open(read_data=MOCK_CONFIG)
  )
  def test_load(self):
    self.configuration.validate = mock.MagicMock()
    result = self.configuration.load()
    self.assertEqual(result, MOCK_JSON)
    self.configuration.validate.assert_called_once_with()


class TestUserConfigurationValidate(TestCase):
  """Test the UserConfiguration class validate method."""

  def setUp(self):
    self.configuration = config_file.UserConfiguration()

  def test_valid(self):
    self.configuration.user_config = MOCK_VALID_JSON
    self.configuration.validate()

  def test_invalid(self):
    self.configuration.user_config = MOCK_JSON

    with self.assertRaises(config_file.UserConfigurationException) as exc:
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
