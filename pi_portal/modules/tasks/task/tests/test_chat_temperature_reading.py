"""Test the chat_send_temperature_reading module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import chat_send_temperature_reading
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestChatTemperatureModule(GenericTaskModuleTest):
  """Test the chat_send_temperature_reading module."""

  expected_api_enabled = True
  expected_arg_class = chat_send_temperature_reading.Args
  expected_return_type = None
  expected_routing_label = enums.RoutingLabel.CHAT_SEND_MESSAGE
  expected_type = enums.TaskType.CHAT_SEND_TEMPERATURE_READING
  mock_args = chat_send_temperature_reading.Args(header="Test Header")
  module = chat_send_temperature_reading
