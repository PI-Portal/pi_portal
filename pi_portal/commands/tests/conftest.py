"""Test fixtures for the commands tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from unittest import mock

import pytest
from .. import (
    cron_scheduler,
    door_monitor,
    installer,
    slack_bot,
    temperature_monitor,
    upload_snapshot,
    upload_video,
    version,
)


@pytest.fixture
def mocked_click() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_cron_scheduler() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_door_monitor_factory() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_name() -> str:
  return "/mock/path/mock.file"


@pytest.fixture
def mocked_installer() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_slack_bot() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_slack_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_temperature_monitor_factory() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def cron_instance(
    mocked_cron_scheduler: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> cron_scheduler.CronSchedulerCommand:
  monkeypatch.setattr(
      cron_scheduler.__name__ + ".scheduler.CronScheduler",
      mocked_cron_scheduler,
  )
  return cron_scheduler.CronSchedulerCommand()


@pytest.fixture
def door_monitor_command_instance(
    mocked_door_monitor_factory: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> door_monitor.DoorMonitorCommand:
  monkeypatch.setattr(
      door_monitor.__name__ + ".gpio.DoorMonitorFactory",
      mocked_door_monitor_factory,
  )
  return door_monitor.DoorMonitorCommand()


@pytest.fixture
def installer_command_instance(
    mocked_click: mock.Mock,
    mocked_file_name: str,
    mocked_installer: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> installer.InstallerCommand:
  monkeypatch.setattr(
      installer.__name__ + ".click",
      mocked_click,
  )
  monkeypatch.setattr(
      installer.__name__ + ".pi_portal_installer.Installer",
      mocked_installer,
  )
  return installer.InstallerCommand(mocked_file_name, False)


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
def temperature_monitor_command_instance(
    mocked_temperature_monitor_factory: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> temperature_monitor.TemperatureMonitorCommand:
  monkeypatch.setattr(
      temperature_monitor.__name__ + ".gpio.TemperatureMonitorFactory",
      mocked_temperature_monitor_factory,
  )
  return temperature_monitor.TemperatureMonitorCommand()


@pytest.fixture
def upload_snapshot_command_instance(
    mocked_file_name: str,
    mocked_slack_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> upload_snapshot.UploadSnapshotCommand:
  monkeypatch.setattr(
      upload_snapshot.__name__ + ".slack.SlackClient",
      mocked_slack_client,
  )
  return upload_snapshot.UploadSnapshotCommand(mocked_file_name)


@pytest.fixture
def upload_video_command_instance(
    mocked_file_name: str,
    mocked_slack_client: mock.Mock,
    mocked_shutil: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> upload_video.UploadVideoCommand:
  monkeypatch.setattr(
      upload_video.__name__ + ".slack.SlackClient",
      mocked_slack_client,
  )
  monkeypatch.setattr(
      upload_video.__name__ + ".shutil",
      mocked_shutil,
  )
  return upload_video.UploadVideoCommand(mocked_file_name)


@pytest.fixture
def version_command_instance(
    mocked_click: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> version.VersionCommand:
  monkeypatch.setattr(
      version.__name__ + ".click",
      mocked_click,
  )
  return version.VersionCommand()
