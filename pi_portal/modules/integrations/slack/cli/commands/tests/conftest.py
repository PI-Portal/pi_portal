"""Test fixtures for the chat CLI command modules tests."""
# pylint: disable=redefined-outer-name

from typing import Callable, Dict
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from .. import (
    command_arm,
    command_disarm,
    command_help,
    command_id,
    command_restart,
    command_snapshot,
    command_status,
    command_temperature,
    command_uptime,
)


@pytest.fixture
def mocked_linux_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_motion_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_temperature_log_file_reader() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_uptime_subcommands() -> Dict[str, mock.Mock]:
  return {
      "BotUptimeCommand": mock.Mock(),
      "ContactSwitchMonitorUptimeCommand": mock.Mock(),
      "TaskSchedulerUptimeCommand": mock.Mock(),
      "TempMonitorUptimeCommand": mock.Mock(),
  }


@pytest.fixture
def arm_command_instance(
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> command_arm.ArmCommand:
  setup_process_command_mocks()
  return command_arm.ArmCommand(mocked_chat_bot)


@pytest.fixture
def disarm_command_instance(
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> command_disarm.DisarmCommand:
  setup_process_command_mocks()
  return command_disarm.DisarmCommand(mocked_chat_bot)


@pytest.fixture
def help_command_instance(
    mocked_chat_bot: mock.Mock,
) -> command_help.HelpCommand:
  return command_help.HelpCommand(mocked_chat_bot)


@pytest.fixture
def id_command_instance(
    mocked_chat_bot: mock.Mock,
    mocked_state: state.State,
) -> command_id.IDCommand:
  state.State().log_uuid = mocked_state.log_uuid
  return command_id.IDCommand(mocked_chat_bot)


@pytest.fixture
def restart_command_instance(
    mocked_chat_bot: mock.Mock,
    mocked_os_module: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> command_restart.RestartCommand:
  monkeypatch.setattr(
      command_restart.__name__ + ".os",
      mocked_os_module,
  )
  return command_restart.RestartCommand(mocked_chat_bot)


@pytest.fixture
def snapshot_command_instance(
    mocked_chat_bot: mock.Mock,
    mocked_motion_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
    setup_process_command_mocks: Callable[[], None],
) -> command_snapshot.SnapshotCommand:
  monkeypatch.setattr(
      command_snapshot.__name__ + ".motion_client.MotionClient",
      mocked_motion_client,
  )
  setup_process_command_mocks()
  return command_snapshot.SnapshotCommand(mocked_chat_bot)


@pytest.fixture
def status_command_instance(
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> command_status.StatusCommand:
  setup_process_command_mocks()
  return command_status.StatusCommand(mocked_chat_bot)


@pytest.fixture
def temperature_command_instance(
    mocked_chat_bot: mock.Mock,
    mocked_state: state.State,
    mocked_temperature_log_file_reader: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> command_temperature.TemperatureCommand:
  state.State().user_config = mocked_state.user_config
  monkeypatch.setattr(
      command_temperature.__name__ +
      ".temperature_monitor_logfile.TemperatureMonitorLogFileReader",
      mocked_temperature_log_file_reader,
  )
  return command_temperature.TemperatureCommand(mocked_chat_bot)


@pytest.fixture
def uptime_command_instance(
    mocked_chat_bot: mock.Mock,
    mocked_linux_module: mock.Mock,
    mocked_uptime_subcommands: Dict[str, mock.Mock],
    monkeypatch: pytest.MonkeyPatch,
    setup_process_command_mocks: Callable[[], None],
) -> command_uptime.UptimeCommand:
  for class_name, mocked_class in mocked_uptime_subcommands.items():
    monkeypatch.setattr(
        command_uptime.__name__ + "." + class_name,
        mocked_class,
    )
  monkeypatch.setattr(
      command_uptime.__name__ + ".linux",
      mocked_linux_module,
  )
  setup_process_command_mocks()
  return command_uptime.UptimeCommand(mocked_chat_bot)
