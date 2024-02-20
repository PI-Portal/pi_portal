"""Test fixtures for the chat CLI subcommands modules tests."""
# pylint: disable=redefined-outer-name

from typing import Callable
from unittest import mock

import pytest
from .. import (
    uptime_chat_bot,
    uptime_contact_switch_monitor,
    uptime_task_scheduler,
    uptime_temp_monitor,
)


@pytest.fixture
def uptime_chat_bot_instance(
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> uptime_chat_bot.BotUptimeCommand:
  setup_process_command_mocks()
  return uptime_chat_bot.BotUptimeCommand(mocked_chat_bot)


@pytest.fixture
def uptime_contact_switch_monitor_instance(
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> uptime_contact_switch_monitor.ContactSwitchMonitorUptimeCommand:
  setup_process_command_mocks()
  return uptime_contact_switch_monitor.ContactSwitchMonitorUptimeCommand(
      mocked_chat_bot
  )


@pytest.fixture
def uptime_task_scheduler_instance(
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> uptime_task_scheduler.TaskSchedulerUptimeCommand:
  setup_process_command_mocks()
  return uptime_task_scheduler.TaskSchedulerUptimeCommand(mocked_chat_bot)


@pytest.fixture
def uptime_temp_monitor_instance(
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> uptime_temp_monitor.TempMonitorUptimeCommand:
  setup_process_command_mocks()
  return uptime_temp_monitor.TempMonitorUptimeCommand(mocked_chat_bot)
