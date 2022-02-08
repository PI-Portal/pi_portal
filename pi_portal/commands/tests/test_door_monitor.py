"""Test the DoorMonitorCommand class."""

from unittest import mock

from pi_portal.commands.bases.tests.fixtures import command_harness
from .. import door_monitor


class TestDoorMonitorCommand(command_harness.CommandBaseTestHarness):
  """Test the DoorMonitorCommand class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = door_monitor.DoorMonitorCommand

  @mock.patch(door_monitor.__name__ + ".gpio")
  def test_invoke(self, m_module: mock.Mock) -> None:

    self.instance.invoke()

    m_factory_instance = m_module.DoorMonitorFactory.return_value
    m_monitor_instance = m_factory_instance.create.return_value

    m_module.DoorMonitorFactory.assert_called_once_with()
    m_factory_instance.create.assert_called_once_with()
    m_monitor_instance.start.assert_called_once_with()
