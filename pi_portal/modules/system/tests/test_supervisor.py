"""Test the SupervisorClient Class."""

from typing import cast
from unittest import mock

import pytest
from pi_portal.modules.python.xmlrpc import patched_client
from pi_portal.modules.system import supervisor, supervisor_config


class TestSupervisorClient:
  """Test the SupervisorClient class."""

  mock_status = supervisor_config.ProcessStatus("RUNNING")
  mock_start = "00:00:00"
  mock_process_info = supervisor.TypeSupervisorProcessInfo(
      statename=mock_status,
      start=mock_start,
  )

  def test_initialize__attributes(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    assert supervisor_instance.server == cast(
        patched_client.Server,
        mocked_supervisor_server.return_value,
    )

  def test_start__success__calls_server_method(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    supervisor_instance.start(supervisor_config.ProcessList.CAMERA)

    mocked_supervisor_server.return_value.supervisor.startProcess.\
        assert_called_once_with(
          supervisor_config.ProcessList.CAMERA.value
        )

  def test_start__error__throws_exception(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    mocked_supervisor_server.return_value.supervisor.startProcess.\
        side_effect = (
          patched_client.Fault(1, "MockFaultError")
        )
    with pytest.raises(supervisor.SupervisorException):

      supervisor_instance.start(supervisor_config.ProcessList.CAMERA)

  def test_stop__success__calls_server_method(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    supervisor_instance.stop(supervisor_config.ProcessList.CAMERA)

    mocked_supervisor_server.return_value.supervisor.stopProcess.\
        assert_called_once_with(
          supervisor_config.ProcessList.CAMERA.value
        )

  def test_stop__error__throws_exception(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    mocked_supervisor_server.return_value.supervisor.stopProcess.\
        side_effect = (
            patched_client.Fault(1, "MockFaultError")
        )
    with pytest.raises(supervisor.SupervisorException):

      supervisor_instance.stop(supervisor_config.ProcessList.CAMERA)

  def test_status__success__returns_correct_status(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    mocked_supervisor_server.return_value.supervisor.getProcessInfo.\
        return_value = self.mock_process_info

    result = supervisor_instance.status(supervisor_config.ProcessList.CAMERA)

    mocked_supervisor_server.return_value.supervisor.getProcessInfo.\
        assert_called_once_with(
          supervisor_config.ProcessList.CAMERA.value
        )
    assert result == self.mock_status

  def test_status__error__throws_exception(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    mocked_supervisor_server.return_value.supervisor.getProcessInfo.\
        side_effect = (
          patched_client.Fault(1, "MockFaultError")
        )
    with pytest.raises(supervisor.SupervisorException):

      supervisor_instance.status(supervisor_config.ProcessList.CAMERA)

  def test_start_time__success__returns_correct_time(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    mocked_supervisor_server.return_value.supervisor.getProcessInfo.\
        return_value = self.mock_process_info

    result = supervisor_instance.start_time(
        supervisor_config.ProcessList.CONTACT_SWITCH_MONITOR
    )

    mocked_supervisor_server.return_value.supervisor.getProcessInfo.\
        assert_called_once_with(
          supervisor_config.ProcessList.CONTACT_SWITCH_MONITOR.value
        )
    assert result == self.mock_start

  def test_start_time__error__throws_exception(
      self,
      mocked_supervisor_server: mock.Mock,
      supervisor_instance: supervisor.SupervisorClient,
  ) -> None:
    mocked_supervisor_server.return_value.supervisor.getProcessInfo.\
        side_effect = (
            patched_client.Fault(1, "MockFaultError")
        )
    with pytest.raises(supervisor.SupervisorException):

      supervisor_instance.start_time(
          supervisor_config.ProcessList.CONTACT_SWITCH_MONITOR
      )
