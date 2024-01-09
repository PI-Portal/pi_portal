"""Test the SlackClientConfiguration class."""

from pi_portal.modules.integrations.slack import config


class TestSlackClient:
  """Test the SlackClientConfiguration class."""

  def test_initialize(self) -> None:
    configuration = config.SlackClientConfiguration()

    assert configuration.interval == 1
    assert configuration.upload_file_title == "Motion Upload"
