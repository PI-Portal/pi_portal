"""Test the BotUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ...bases.tests.fixtures import process_uptime_command_harness
from .. import slack_bot_uptime


class TestBotUptimeCommand(
    process_uptime_command_harness.ProcessUptimeCommandBaseTestHarness
):
  """Test the BotUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.BOT

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = slack_bot_uptime.BotUptimeCommand
