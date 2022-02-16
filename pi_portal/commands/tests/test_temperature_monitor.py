"""Test the TemperatureMonitorCommand class."""

from unittest import mock

from pi_portal.commands.bases.tests.fixtures import command_harness
from .. import temperature_monitor
from ..mixins import state


class TestTemperatureMonitorCommand(command_harness.CommandBaseTestHarness):
  """Test the TemperatureMonitorCommand class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = temperature_monitor.TemperatureMonitorCommand

  def test_mixins(self) -> None:
    self.assertIsInstance(self.instance, state.CommandManagedStateMixin)

  @mock.patch(temperature_monitor.__name__ + ".gpio")
  def test_invoke(self, m_module: mock.Mock) -> None:

    self.instance.invoke()

    m_factory_instance = m_module.TemperatureMonitorFactory.return_value
    m_monitor_instance = m_factory_instance.create.return_value

    m_module.TemperatureMonitorFactory.assert_called_once_with()
    m_factory_instance.create.assert_called_once_with()
    m_monitor_instance.start.assert_called_once_with()
