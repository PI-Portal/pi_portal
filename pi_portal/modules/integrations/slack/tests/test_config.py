"""Test the SlackClientConfiguration class."""

from unittest import TestCase

from pi_portal.modules.integrations.slack import config


class TestSlackClient(TestCase):
  """Test the SlackClientConfiguration class."""

  def test_initialize(self) -> None:
    configuration = config.SlackClientConfiguration()
    self.assertEqual(configuration.interval, 1)
    self.assertEqual(configuration.upload_file_title, "Motion Upload")
