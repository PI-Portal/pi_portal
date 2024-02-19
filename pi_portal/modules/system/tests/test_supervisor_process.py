"""Test SupervisorProcess class."""

from typing import List
from unittest import mock

import pytest
from freezegun import freeze_time
from pi_portal.modules.system import supervisor_config, supervisor_process


class TestSupervisorProcess:
  """Test the SupervisorProcess class."""

  def test_initialize__attributes(
      self, supervisor_process_instance: supervisor_process.SupervisorProcess
  ) -> None:
    assert supervisor_process_instance.process_name == (
        supervisor_config.ProcessList.BOT
    )

  def test_initialize__supervisor_client(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
  ) -> None:
    assert supervisor_process_instance.client == (
        mocked_supervisor_client.return_value
    )
    mocked_supervisor_client.assert_called_once_with()

  @pytest.mark.parametrize(
      "test_status", [
          supervisor_config.ProcessStatus.FATAL,
          supervisor_config.ProcessStatus.SHUTDOWN,
          supervisor_config.ProcessStatus.STOPPED,
      ]
  )
  def test_start__vary_state__calls_client_correctly(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
      test_status: supervisor_config.ProcessStatus,
  ) -> None:
    mocked_supervisor_client.return_value.status.return_value = test_status

    supervisor_process_instance.start()

    mocked_supervisor_client.return_value.status.assert_called_once_with(
        supervisor_process_instance.process_name
    )
    mocked_supervisor_client.return_value.start.assert_called_once_with(
        supervisor_process_instance.process_name
    )

  @pytest.mark.parametrize(
      "test_status", [
          supervisor_config.ProcessStatus.RUNNING,
          supervisor_config.ProcessStatus.RESTARTING,
          supervisor_config.ProcessStatus.STARTING,
      ]
  )
  def test_start__vary_state__raises_exception(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
      test_status: supervisor_config.ProcessStatus,
  ) -> None:
    mocked_supervisor_client.return_value.status.return_value = test_status

    with pytest.raises(supervisor_process.SupervisorProcessException):
      supervisor_process_instance.start()

    mocked_supervisor_client.return_value.status.assert_called_once_with(
        supervisor_process_instance.process_name
    )
    mocked_supervisor_client.return_value.start.assert_not_called()

  @pytest.mark.parametrize(
      "test_status", [
          supervisor_config.ProcessStatus.RUNNING,
          supervisor_config.ProcessStatus.STARTING,
      ]
  )
  def test_stop__vary_state__calls_client_correctly(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
      test_status: supervisor_config.ProcessStatus,
  ) -> None:
    mocked_supervisor_client.return_value.status.return_value = test_status

    supervisor_process_instance.stop()

    mocked_supervisor_client.return_value.status.assert_called_once_with(
        supervisor_process_instance.process_name
    )
    mocked_supervisor_client.return_value.stop.assert_called_once_with(
        supervisor_process_instance.process_name
    )

  @pytest.mark.parametrize(
      "test_status", [
          supervisor_config.ProcessStatus.FATAL,
          supervisor_config.ProcessStatus.SHUTDOWN,
          supervisor_config.ProcessStatus.STOPPED,
      ]
  )
  def test_stop__vary_state__raises_exception(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
      test_status: supervisor_config.ProcessStatus,
  ) -> None:
    mocked_supervisor_client.return_value.status.return_value = test_status

    with pytest.raises(supervisor_process.SupervisorProcessException):
      supervisor_process_instance.stop()

    mocked_supervisor_client.return_value.status.assert_called_once_with(
        supervisor_process_instance.process_name
    )
    mocked_supervisor_client.return_value.stop.assert_not_called()

  @pytest.mark.parametrize(
      "test_status",
      supervisor_config.ProcessStatus,
  )
  def test_status__vary_state__returns_correct_value(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
      test_status: supervisor_config.ProcessStatus,
  ) -> None:
    mocked_supervisor_client.return_value.status.return_value = test_status

    result = supervisor_process_instance.status()

    mocked_supervisor_client.return_value.status.assert_called_once_with(
        supervisor_process_instance.process_name
    )
    assert result == test_status.value

  @pytest.mark.parametrize(
      "status_range,test_status", [
          [
              [supervisor_config.ProcessStatus.STOPPED],
              supervisor_config.ProcessStatus.RUNNING,
          ],
          [
              [supervisor_config.ProcessStatus.RUNNING],
              supervisor_config.ProcessStatus.RUNNING,
          ],
      ]
  )
  def test_status_in__vary_state__returns_correct_value(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
      status_range: List[supervisor_config.ProcessStatus],
      test_status: supervisor_config.ProcessStatus,
  ) -> None:
    mocked_supervisor_client.return_value.status.return_value = test_status

    result = supervisor_process_instance.status_in(status_range)

    assert result == (test_status in status_range)

  @freeze_time("2021-11-21-04:30:00")
  @pytest.mark.parametrize(
      "test_status",
      [
          supervisor_config.ProcessStatus.RUNNING,
      ],
  )
  def test_uptime__vary_state__returns_correct_value(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
      test_status: supervisor_config.ProcessStatus,
  ) -> None:
    mocked_supervisor_client.return_value.status.return_value = test_status
    mocked_supervisor_client.return_value.start_time.return_value = "1637288711"

    result = supervisor_process_instance.uptime()

    mocked_supervisor_client.return_value.status.assert_called_once_with(
        supervisor_process_instance.process_name
    )
    assert result == "2 days"

  @pytest.mark.parametrize(
      "test_status",
      [
          supervisor_config.ProcessStatus.FATAL,
          supervisor_config.ProcessStatus.RESTARTING,
          supervisor_config.ProcessStatus.SHUTDOWN,
          supervisor_config.ProcessStatus.STARTING,
          supervisor_config.ProcessStatus.STOPPED,
      ],
  )
  def test_uptime__vary_state__return_correct_message(
      self,
      supervisor_process_instance: supervisor_process.SupervisorProcess,
      mocked_supervisor_client: mock.Mock,
      test_status: supervisor_config.ProcessStatus,
  ) -> None:
    mocked_supervisor_client.return_value.status.return_value = test_status

    result = supervisor_process_instance.uptime()

    mocked_supervisor_client.return_value.status.assert_called_once_with(
        supervisor_process_instance.process_name
    )
    assert result == supervisor_process_instance.uptime_when_stopped
