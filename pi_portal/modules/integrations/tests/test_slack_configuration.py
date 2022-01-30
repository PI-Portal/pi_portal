"""Test Slack ClientConfiguration class."""

from unittest import TestCase

from pi_portal.modules.integrations import slack
from pi_portal.modules.logger import LOG_UUID


class TestSlackClient(TestCase):
  """Test the ClientConfiguration class."""

  def test_initialize(self):
    configuration = slack.ClientConfiguration()
    self.assertEqual(configuration.log_uuid, LOG_UUID)
    self.assertEqual(configuration.interval, 1)
    self.assertEqual(configuration.upload_file_title, "Motion Upload")
