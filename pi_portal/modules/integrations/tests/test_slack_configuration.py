"""Test Slack ClientConfiguration class."""

from unittest import TestCase

from pi_portal.modules.integrations import slack


class TestSlackClient(TestCase):
  """Test the ClientConfiguration class."""

  def test_initialize(self):
    configuration = slack.ClientConfiguration()
    self.assertEqual(configuration.interval, 1)
    self.assertEqual(configuration.upload_file_title, "Motion Upload")
