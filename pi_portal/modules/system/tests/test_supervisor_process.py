"""Test SupervisorProcess Class."""

from typing import cast
from unittest import TestCase, mock

from freezegun import freeze_time
from pi_portal.modules.system import (
    supervisor,
    supervisor_config,
    supervisor_process,
)


class TestSupervisorProcess(TestCase):
  """Test the SupervisorProcess class."""

  def setUp(self) -> None:
    self.mock_process = supervisor_config.ProcessList.BOT
    with mock.patch(
        supervisor_process.__name__ + ".supervisor.SupervisorClient"
    ):
      self.instance = supervisor_process.SupervisorProcess(self.mock_process)

  def _mocked_client(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.client)

  def test_initialize(self) -> None:
    instance = supervisor_process.SupervisorProcess(self.mock_process)
    self.assertIsInstance(instance.client, supervisor.SupervisorClient)
    self.assertEqual(instance.process_name, self.mock_process)

  def test_start_is_stopped(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.STOPPED
    self.instance.start()

    self._mocked_client().status.assert_called_once_with(self.mock_process)
    self._mocked_client().start.assert_called_once_with(self.mock_process)

  def test_start_is_running(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.RUNNING

    with self.assertRaises(supervisor_process.SupervisorProcessException):
      self.instance.start()

    self._mocked_client().status.assert_called_once_with(self.mock_process)
    self._mocked_client().start.assert_not_called()

  def test_start_is_restarting(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.RESTARTING

    with self.assertRaises(supervisor_process.SupervisorProcessException):
      self.instance.start()

    self._mocked_client().status.assert_called_once_with(self.mock_process)
    self._mocked_client().start.assert_not_called()

  def test_stop_is_running(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.RUNNING
    self.instance.stop()

    self._mocked_client().status.assert_called_once_with(self.mock_process)
    self._mocked_client().stop.assert_called_once_with(self.mock_process)

  def test_stop_is_restarting(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.RESTARTING

    self.instance.stop()

    self._mocked_client().status.assert_called_once_with(self.mock_process)
    self._mocked_client().stop.assert_called_once_with(self.mock_process)

  def test_stop_is_stopped(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.STOPPED

    with self.assertRaises(supervisor_process.SupervisorProcessException):
      self.instance.stop()

    self._mocked_client().status.assert_called_once_with(self.mock_process)
    self._mocked_client().stop.assert_not_called()

  def test_stop_is_fatal(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.FATAL

    with self.assertRaises(supervisor_process.SupervisorProcessException):
      self.instance.stop()

    self._mocked_client().status.assert_called_once_with(self.mock_process)
    self._mocked_client().stop.assert_not_called()

  def test_status_running(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.RUNNING

    result = self.instance.status()

    self.assertEqual(result, supervisor_config.ProcessStatus.RUNNING.value)
    self._mocked_client().status.assert_called_once_with(self.mock_process)

  def test_status_stopped(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.STOPPED

    result = self.instance.status()

    self.assertEqual(result, supervisor_config.ProcessStatus.STOPPED.value)
    self._mocked_client().status.assert_called_once_with(self.mock_process)

  def test_status_in_true(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.RUNNING

    result = self.instance.status_in(
        [
            supervisor_config.ProcessStatus.SHUTDOWN,
            supervisor_config.ProcessStatus.RUNNING
        ],
    )

    self.assertTrue(result)
    self._mocked_client().status.assert_called_once_with(self.mock_process)

  def test_status_in_false(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.FATAL

    result = self.instance.status_in(
        [
            supervisor_config.ProcessStatus.SHUTDOWN,
            supervisor_config.ProcessStatus.RUNNING
        ],
    )

    self.assertFalse(result)
    self._mocked_client().status.assert_called_once_with(self.mock_process)

  @freeze_time("2021-11-18-22:30:00")
  def test_uptime_running(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.RUNNING
    self._mocked_client().uptime.return_value = "1637288711"

    result = self.instance.uptime()

    self._mocked_client().uptime.assert_called_once_with(self.mock_process)
    self.assertEqual(result, "3 hours")

  def test_uptime_stopping(self) -> None:
    self._mocked_client(
    ).status.return_value = supervisor_config.ProcessStatus.STOPPED

    result = self.instance.uptime()

    self._mocked_client().uptime.assert_not_called()
    self.assertEqual(result, self.instance.uptime_when_stopped)
