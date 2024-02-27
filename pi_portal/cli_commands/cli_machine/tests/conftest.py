"""Test fixtures for the machine cli commands tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from typing import Callable
from unittest import mock

import pytest
from pi_portal.cli_commands.mixins import require_task_scheduler
from .. import (
    chatbot,
    contact_switch_monitor,
    task_scheduler,
    temperature_monitor,
    upload_snapshot,
    upload_video,
)


@pytest.fixture
def mocked_chatbot() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_contact_switch_monitor_factory() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_name() -> str:
  return "/mock/path/mock.file"


@pytest.fixture
def mocked_require_task_scheduler() -> mock.Mock:
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
def setup_require_task_scheduler_mocks(
    mocked_require_task_scheduler: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        require_task_scheduler.__name__ +
        ".CommandTaskSchedulerMixin.require_task_scheduler",
        mocked_require_task_scheduler,
    )

  return setup


@pytest.fixture
def chatbot_command_instance(
    mocked_chatbot: mock.Mock,
    setup_require_task_scheduler_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> chatbot.ChatBotCommand:
  monkeypatch.setattr(
      chatbot.__name__ + ".ChatBot",
      mocked_chatbot,
  )
  setup_require_task_scheduler_mocks()
  return chatbot.ChatBotCommand()


@pytest.fixture
def contact_switch_monitor_command_instance(
    mocked_contact_switch_monitor_factory: mock.Mock,
    setup_require_task_scheduler_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> contact_switch_monitor.ContactSwitchMonitorCommand:
  monkeypatch.setattr(
      contact_switch_monitor.__name__ + ".gpio.ContactSwitchMonitorFactory",
      mocked_contact_switch_monitor_factory,
  )
  setup_require_task_scheduler_mocks()
  return contact_switch_monitor.ContactSwitchMonitorCommand()


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
    setup_require_task_scheduler_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> temperature_monitor.TemperatureMonitorCommand:
  monkeypatch.setattr(
      temperature_monitor.__name__ + ".gpio.TemperatureSensorMonitorFactory",
      mocked_temperature_sensor_monitor_factory,
  )
  setup_require_task_scheduler_mocks()
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
