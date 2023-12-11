"""Test Supervisor SlackClient Class."""

from typing import cast
from unittest import TestCase, mock

from pi_portal.modules.python.xmlrpc import patched_client
from pi_portal.modules.system import supervisor, supervisor_config


class TestSupervisorClient(TestCase):
  """Test the SupervisorClient class."""

  mock_state = supervisor_config.ProcessStatus("RUNNING")
  mock_start = "00:00:00"

  def setUp(self) -> None:
    self.supervisor_client = supervisor.SupervisorClient()
    self.supervisor_client.server = mock.MagicMock()

  def _mock_server(self) -> mock.Mock:
    return cast(mock.Mock, self.supervisor_client.server)

  def create_mock_process_info(self) -> supervisor.TypeSupervisorProcessInfo:
    return supervisor.TypeSupervisorProcessInfo(
        statename=self.mock_state,
        start=self.mock_start,
    )

  def test_initialize(self) -> None:
    client = supervisor.SupervisorClient()
    self.assertIsInstance(client.server, patched_client.Server)

  def test_start(self) -> None:
    self.supervisor_client.start(supervisor_config.ProcessList.CAMERA)
    self._mock_server().supervisor.startProcess.\
      assert_called_once_with(
        supervisor_config.ProcessList.CAMERA.value
      )

  def test_start_error(self) -> None:
    self._mock_server().supervisor.startProcess.side_effect = (
        patched_client.Fault(1, "MockFaultError")
    )
    with self.assertRaises(supervisor.SupervisorException):
      self.supervisor_client.start(supervisor_config.ProcessList.CAMERA)

  def test_stop(self) -> None:
    self.supervisor_client.stop(supervisor_config.ProcessList.CAMERA)
    self._mock_server().supervisor.stopProcess.\
      assert_called_once_with(
        supervisor_config.ProcessList.CAMERA.value
      )

  def test_stop_error(self) -> None:
    self._mock_server().supervisor.stopProcess.side_effect = (
        patched_client.Fault(1, "MockFaultError")
    )
    with self.assertRaises(supervisor.SupervisorException):
      self.supervisor_client.stop(supervisor_config.ProcessList.CAMERA)

  def test_status(self) -> None:
    self._mock_server().supervisor.getProcessInfo.return_value = \
      self.create_mock_process_info()
    result = self.supervisor_client.status(supervisor_config.ProcessList.CAMERA)
    self._mock_server().supervisor.getProcessInfo.\
      assert_called_once_with(
        supervisor_config.ProcessList.CAMERA.value
      )
    self.assertEqual(result, self.mock_state)

  def test_status_error(self) -> None:
    self._mock_server().supervisor.getProcessInfo.side_effect = (
        patched_client.Fault(1, "MockFaultError")
    )
    with self.assertRaises(supervisor.SupervisorException):
      self.supervisor_client.status(supervisor_config.ProcessList.CAMERA)

  def test_start_time(self) -> None:
    self._mock_server().supervisor.getProcessInfo.return_value = \
      self.create_mock_process_info()
    result = self.supervisor_client.start_time(
        supervisor_config.ProcessList.DOOR_MONITOR
    )
    self._mock_server().supervisor.getProcessInfo.\
      assert_called_once_with(
        supervisor_config.ProcessList.DOOR_MONITOR.value
      )
    self.assertEqual(result, self.mock_start)

  def test_start_time_error(self) -> None:
    self._mock_server().supervisor.getProcessInfo.side_effect = (
        patched_client.Fault(1, "MockFaultError")
    )
    with self.assertRaises(supervisor.SupervisorException):
      self.supervisor_client.start_time(
          supervisor_config.ProcessList.DOOR_MONITOR
      )
