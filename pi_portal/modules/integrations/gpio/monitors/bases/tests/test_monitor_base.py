"""Test GPIOMonitorBase class."""

from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal.modules.mixins import write_log_file
from .. import monitor_base
from .conftest import Interrupt, TypeGenericGpioMonitor


class TestGPIOMonitorBase:
  """Test GPIOMonitorBase class."""

  def test_initialize__attributes(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_gpio_pins: List[mock.Mock],
  ) -> None:
    assert concrete_gpio_monitor_instance.gpio_poll_interval == 0.5
    assert concrete_gpio_monitor_instance.gpio_log_changes_only is True
    assert concrete_gpio_monitor_instance.gpio_pins == mocked_gpio_pins
    assert concrete_gpio_monitor_instance.logger_name == "test_logger"
    assert concrete_gpio_monitor_instance.log_file_path == (
        "/var/log/non_existent.log"
    )

  def test_initialize__inheritance(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
  ) -> None:
    assert isinstance(
        concrete_gpio_monitor_instance,
        monitor_base.GPIOMonitorBase,
    )
    assert isinstance(
        concrete_gpio_monitor_instance,
        write_log_file.LogFileWriter,
    )

  def test_initialize__logger(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_configure_logger: mock.Mock,
      mocked_logger: mock.Mock,
  ) -> None:
    assert concrete_gpio_monitor_instance.log == mocked_logger
    mocked_configure_logger.assert_called_once_with()

  @pytest.mark.usefixtures("concrete_gpio_monitor_instance")
  def test_initialize__rpi_module(
      self,
      mocked_rpi_module: mock.Mock,
  ) -> None:
    mocked_rpi_module.GPIO.setmode.assert_called_once_with(
        mocked_rpi_module.GPIO.BCM
    )

  def test_initialize__slack_client(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_slack_client: mock.Mock,
  ) -> None:
    assert concrete_gpio_monitor_instance.slack_client == (
        mocked_slack_client.return_value
    )
    mocked_slack_client.assert_called_once_with()

  def test_start__single_run__changes_only__has_changed__updates_gpio_state(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_sleep: mock.Mock,
      mocked_gpio_pins: List[mock.Mock],
  ) -> None:
    setattr(concrete_gpio_monitor_instance, "gpio_log_changes_only", True)
    mocked_sleep.side_effect = [Interrupt]
    for pin in mocked_gpio_pins:
      pin.has_changed.return_value = True

    with pytest.raises(Interrupt):
      concrete_gpio_monitor_instance.start()

    for pin in mocked_gpio_pins:
      pin.poll.assert_called_once_with()
      pin.has_changed.assert_called_once_with()

  def test_start__single_run__changes_only__has_changed__logs_gpio_state(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_sleep: mock.Mock,
      mocked_gpio_pins: List[mock.Mock],
      mocked_stream: StringIO,
  ) -> None:
    setattr(concrete_gpio_monitor_instance, "gpio_log_changes_only", True)
    mocked_sleep.side_effect = [Interrupt]
    for pin in mocked_gpio_pins:
      pin.has_changed.return_value = True

    with pytest.raises(Interrupt):
      concrete_gpio_monitor_instance.start()

    assert mocked_stream.getvalue() == "".join(
        [
            f"INFO - {pin.pin_name} -> {pin.current_state}\n"
            for pin in mocked_gpio_pins
        ]
    )

  def test_start__single_run__changes_only__has_not_changed__updates_gpio_state(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_sleep: mock.Mock,
      mocked_gpio_pins: List[mock.Mock],
  ) -> None:
    setattr(concrete_gpio_monitor_instance, "gpio_log_changes_only", True)
    mocked_sleep.side_effect = [Interrupt]
    for pin in mocked_gpio_pins:
      pin.has_changed.return_value = False

    with pytest.raises(Interrupt):
      concrete_gpio_monitor_instance.start()

    for pin in mocked_gpio_pins:
      pin.poll.assert_called_once_with()
      pin.has_changed.assert_called_once_with()

  def test_start__single_run__changes_only__has_not_changed__does_not_log(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_sleep: mock.Mock,
      mocked_gpio_pins: List[mock.Mock],
      mocked_stream: StringIO,
  ) -> None:
    setattr(concrete_gpio_monitor_instance, "gpio_log_changes_only", True)
    mocked_sleep.side_effect = [Interrupt]
    for pin in mocked_gpio_pins:
      pin.has_changed.return_value = False

    with pytest.raises(Interrupt):
      concrete_gpio_monitor_instance.start()

    assert mocked_stream.getvalue() == ""

  def test_start__single_run__not_changes_only__updates_gpio_state(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_sleep: mock.Mock,
      mocked_gpio_pins: List[mock.Mock],
  ) -> None:
    setattr(concrete_gpio_monitor_instance, "gpio_log_changes_only", False)
    mocked_sleep.side_effect = [Interrupt]

    with pytest.raises(Interrupt):
      concrete_gpio_monitor_instance.start()

    for pin in mocked_gpio_pins:
      pin.poll.assert_called_once_with()
      pin.has_changed.assert_not_called()

  def test_start__single_run__not_changes_only__logs_gpio_state(
      self,
      concrete_gpio_monitor_instance: TypeGenericGpioMonitor,
      mocked_sleep: mock.Mock,
      mocked_gpio_pins: List[mock.Mock],
      mocked_stream: StringIO,
  ) -> None:
    setattr(concrete_gpio_monitor_instance, "gpio_log_changes_only", False)
    mocked_sleep.side_effect = [Interrupt]

    with pytest.raises(Interrupt):
      concrete_gpio_monitor_instance.start()

    assert mocked_stream.getvalue() == "".join(
        [
            f"INFO - {pin.pin_name} -> {pin.current_state}\n"
            for pin in mocked_gpio_pins
        ]
    )
