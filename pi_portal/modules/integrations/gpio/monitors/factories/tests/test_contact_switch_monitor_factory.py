"""Tests for the ContactSwitchMonitorFactory class."""

from unittest import mock

from pi_portal.modules.integrations.gpio.monitors import contact_switch_monitor
from pi_portal.modules.integrations.gpio.monitors.factories.bases import (
    monitor_factory_base,
)
from ..contact_switch_monitor_factory import ContactSwitchMonitorFactory


class TestContactSwitchMonitorFactory:
  """Tests for the ContactSwitchMonitorFactory class."""

  def test_initialize__attributes(
      self,
      contact_switch_monitor_factory_instance: ContactSwitchMonitorFactory,
      mocked_state: mock.Mock,
  ) -> None:
    assert contact_switch_monitor_factory_instance.state.user_config == (
        mocked_state.user_config
    )

  def test_initialize__inheritance(
      self,
      contact_switch_monitor_factory_instance: ContactSwitchMonitorFactory,
  ) -> None:
    assert isinstance(
        contact_switch_monitor_factory_instance,
        monitor_factory_base.MonitorFactoryBase,
    )

  def test_create__returns_expected_monitor(
      self,
      contact_switch_monitor_factory_instance: ContactSwitchMonitorFactory,
  ) -> None:
    created_instance = contact_switch_monitor_factory_instance.create()

    assert isinstance(
        created_instance,
        contact_switch_monitor.ContactSwitchMonitor,
    )

  def test_create__returns_monitor_with_expected_gpio_config(
      self,
      contact_switch_monitor_factory_instance: ContactSwitchMonitorFactory,
      mocked_contact_switch_factory_class: mock.Mock,
  ) -> None:
    created_instance = contact_switch_monitor_factory_instance.create()

    mocked_contact_switch_factory_class.assert_called_once_with()
    mocked_contact_switch_factory_class.return_value.create.\
        assert_called_once_with()
    assert created_instance.gpio_pins == (
        mocked_contact_switch_factory_class.return_value.create.return_value
    )
