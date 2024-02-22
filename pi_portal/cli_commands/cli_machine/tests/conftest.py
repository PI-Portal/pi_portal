"""Test fixtures for the machine cli commands tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from unittest import mock

import pytest
from .. import (
    contact_switch_monitor,
    slack_bot,
    task_scheduler,
    temperature_monitor,
    upload_snapshot,
    upload_video,
)


@pytest.fixture
def mocked_contact_switch_monitor_factory() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_name() -> str:
  return "/mock/path/mock.file"


@pytest.fixture
def mocked_slack_bot() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_task_scheduler_service_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_temperature_sensor_monitor_factory() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_uvicorn() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def contact_switch_monitor_command_instance(
    mocked_contact_switch_monitor_factory: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> contact_switch_monitor.ContactSwitchMonitorCommand:
  monkeypatch.setattr(
      contact_switch_monitor.__name__ + ".gpio.ContactSwitchMonitorFactory",
      mocked_contact_switch_monitor_factory,
  )
  return contact_switch_monitor.ContactSwitchMonitorCommand()


@pytest.fixture
def slack_bot_command_instance(
    mocked_slack_bot: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> slack_bot.SlackBotCommand:
  monkeypatch.setattr(
      slack_bot.__name__ + ".slack.SlackBot",
      mocked_slack_bot,
  )
  return slack_bot.SlackBotCommand()


@pytest.fixture
def task_scheduler_command_instance(
    mocked_uvicorn: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> task_scheduler.TaskSchedulerCommand:
  monkeypatch.setattr(
      task_scheduler.__name__ + ".uvicorn",
      mocked_uvicorn,
  )
  return task_scheduler.TaskSchedulerCommand()


@pytest.fixture
def temperature_monitor_command_instance(
    mocked_temperature_sensor_monitor_factory: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> temperature_monitor.TemperatureMonitorCommand:
  monkeypatch.setattr(
      temperature_monitor.__name__ + ".gpio.TemperatureSensorMonitorFactory",
      mocked_temperature_sensor_monitor_factory,
  )
  return temperature_monitor.TemperatureMonitorCommand()


@pytest.fixture
def upload_snapshot_command_instance(
    mocked_file_name: str,
    mocked_task_scheduler_service_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> upload_snapshot.UploadSnapshotCommand:
  monkeypatch.setattr(
      upload_snapshot.__name__ + ".TaskSchedulerServiceClient",
      mocked_task_scheduler_service_client,
  )
  return upload_snapshot.UploadSnapshotCommand(mocked_file_name)


@pytest.fixture
def upload_video_command_instance(
    mocked_file_name: str,
    mocked_task_scheduler_service_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> upload_video.UploadVideoCommand:
  monkeypatch.setattr(
      upload_video.__name__ + ".TaskSchedulerServiceClient",
      mocked_task_scheduler_service_client,
  )
  return upload_video.UploadVideoCommand(mocked_file_name)
