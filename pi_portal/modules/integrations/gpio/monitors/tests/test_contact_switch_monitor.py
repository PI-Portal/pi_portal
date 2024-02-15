"""Test the ContactSwitchMonitor class."""
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal import config
from ..bases import monitor_base
from ..contact_switch_monitor import ContactSwitchMonitor, SwitchState
from .conftest import ContactSwitchScenario, generate_switch_scenario_ids


class TestContactSwitchMonitor:
  """Test the ContactSwitchMonitor class."""

  def test_initialize__attributes(
      self,
      contact_switch_monitor_instance: ContactSwitchMonitor,
      mocked_gpio_pins: List[mock.Mock],
  ) -> None:
    assert contact_switch_monitor_instance.gpio_poll_interval == 0.5
    assert contact_switch_monitor_instance.gpio_log_changes_only is True
    assert contact_switch_monitor_instance.gpio_pins == mocked_gpio_pins
    assert contact_switch_monitor_instance.logger_name == "contact_switch"
    assert contact_switch_monitor_instance.log_file_path == (
        config.LOG_FILE_CONTACT_SWITCH_MONITOR
    )

  def test_initialize__inheritance(
      self,
      contact_switch_monitor_instance: ContactSwitchMonitor,
  ) -> None:
    assert isinstance(
        contact_switch_monitor_instance,
        monitor_base.GPIOMonitorBase,
    )

  @pytest.mark.usefixtures("contact_switch_monitor_instance")
  def test_initialize__rpi_module(
      self,
      mocked_rpi_module: mock.Mock,
  ) -> None:
    mocked_rpi_module.GPIO.setmode.assert_called_once_with(
        mocked_rpi_module.GPIO.BCM
    )

  def test_initialize__slack_client(
      self,
      contact_switch_monitor_instance: ContactSwitchMonitor,
      mocked_slack_client: mock.Mock,
  ) -> None:
    assert contact_switch_monitor_instance.slack_client == (
        mocked_slack_client.return_value
    )
    mocked_slack_client.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario",
      [
          ContactSwitchScenario(name="Front Door", type="Switch", state=False),
          ContactSwitchScenario(name="Back Window", type="Switch", state=True),
      ],
      ids=generate_switch_scenario_ids,
  )
  def test_hook_log_state__vary_gpio_and_state__logging(
      self,
      contact_switch_monitor_instance: ContactSwitchMonitor,
      mocked_gpio_pins: List[mock.Mock],
      mocked_stream: StringIO,
      scenario: ContactSwitchScenario,
  ) -> None:
    mocked_gpio_pins[0].current_state = scenario.state
    mocked_gpio_pins[0].pin_name = scenario.name
    mocked_gpio_pins[0].sensor_type = scenario.type
    expected_state_str = SwitchState(scenario.state).name

    contact_switch_monitor_instance.hook_log_state(mocked_gpio_pins[0])

    assert mocked_stream.getvalue() == (
        f"WARNING - {scenario.type} - {scenario.name} - {expected_state_str} - "
        f"SWITCH:{scenario.name}\n"
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          ContactSwitchScenario(name="Front Door", type="Switch", state=False),
          ContactSwitchScenario(name="Back Window", type="Switch", state=True),
      ],
      ids=generate_switch_scenario_ids,
  )
  def test_hook_log_state__vary_gpio_and_state__calls_slack_client(
      self,
      contact_switch_monitor_instance: ContactSwitchMonitor,
      mocked_gpio_pins: List[mock.Mock],
      mocked_slack_client: mock.Mock,
      scenario: ContactSwitchScenario,
  ) -> None:
    mocked_gpio_pins[0].current_state = scenario.state
    mocked_gpio_pins[0].pin_name = scenario.name
    mocked_gpio_pins[0].sensor_type = scenario.type
    expected_state_str = SwitchState(scenario.state).name

    contact_switch_monitor_instance.hook_log_state(mocked_gpio_pins[0])

    mocked_slack_client.return_value.send_message.assert_called_once_with(
        f":rotating_light: The {scenario.name}"
        f"was {expected_state_str}!"
    )
