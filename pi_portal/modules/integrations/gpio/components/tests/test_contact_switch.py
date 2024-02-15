"""Test the ContactSwitch class."""

from unittest import mock

from .. import contact_switch
from ..bases import input_base


class TestContactSwitch:
  """Test the ContactSwitch class."""

  def test_initialize__attributes(
      self,
      contact_switch_instance: contact_switch.ContactSwitch,
      mocked_pin_name: str,
      mocked_pin_number: int,
  ) -> None:
    assert contact_switch_instance.pin_name == mocked_pin_name
    assert contact_switch_instance.pin_number == mocked_pin_number
    assert contact_switch_instance.last_state is None
    assert contact_switch_instance.current_state is None

  def test_initialize__inheritance(
      self,
      contact_switch_instance: contact_switch.ContactSwitch,
  ) -> None:
    assert isinstance(
        contact_switch_instance,
        input_base.GPIOInputBase,
    )

  def test_initialize__input_setup(
      self,
      contact_switch_instance: contact_switch.ContactSwitch,
      mocked_rpi_gpio_module: mock.Mock,
  ) -> None:
    mocked_rpi_gpio_module.setup.assert_called_once_with(
        contact_switch_instance.pin_number,
        mocked_rpi_gpio_module.IN,
        pull_up_down=mocked_rpi_gpio_module.PUD_UP
    )

  def test_hook_update_state__switch_is_open(
      self,
      contact_switch_instance: contact_switch.ContactSwitch,
      mocked_rpi_gpio_module: mock.Mock,
  ) -> None:
    mocked_rpi_gpio_module.input.return_value = contact_switch_instance.open

    return_value = contact_switch_instance.hook_update_state()

    assert return_value is True

  def test_hook_update_state__switch_is_closed(
      self,
      contact_switch_instance: contact_switch.ContactSwitch,
      mocked_rpi_gpio_module: mock.Mock,
  ) -> None:
    mocked_rpi_gpio_module.input.return_value = 0

    return_value = contact_switch_instance.hook_update_state()

    assert return_value is False
