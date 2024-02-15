"""Test the TemperatureSensorFactory class."""

from unittest import mock

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components import contact_switch
from ..bases import input_factory_base
from ..contact_switch_factory import ContactSwitchFactory


class TestTemperatureSensorFactory:
  """Test the TemperatureSensorFactory class."""

  def test_initiate__attributes(
      self,
      contact_switch_factory_instance: ContactSwitchFactory,
      mocked_state: mock.Mock,
  ) -> None:
    assert isinstance(
        contact_switch_factory_instance.state,
        state.State,
    )
    assert contact_switch_factory_instance.state.user_config == \
        mocked_state.user_config

  def test_initiate__inheritance(
      self,
      contact_switch_factory_instance: ContactSwitchFactory,
  ) -> None:
    assert isinstance(
        contact_switch_factory_instance,
        input_factory_base.GPIOInputFactoryBase,
    )

  def test_create__returns_contact_switches(
      self,
      contact_switch_factory_instance: ContactSwitchFactory,
  ) -> None:
    result = contact_switch_factory_instance.create()

    for switch in result:
      assert isinstance(
          switch,
          contact_switch.ContactSwitch,
      )

  def test_create__returns_correctly_configured_sensors(
      self,
      contact_switch_factory_instance: ContactSwitchFactory,
      mocked_state: mock.Mock,
  ) -> None:
    result = contact_switch_factory_instance.create()

    for index, configured_switch in enumerate(
        mocked_state.state.user_config["SWITCHES"]["CONTACT_SWITCHES"]
    ):
      assert result[index].sensor_type == contact_switch.__name__
      assert result[index].pin_name == configured_switch["NAME"]
      assert result[index].pin_number == configured_switch["GPIO"]
