"""Test fixtures for the processor registry modules."""
# pylint: disable=redefined-outer-name

import logging
from typing import Callable, NamedTuple, Tuple
from unittest import mock

import pytest
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.mixins import chat_client
from .. import (
    archive_logs,
    archive_videos,
    chat_send_message,
    chat_upload_snapshot,
    chat_upload_video,
    file_system_copy,
    file_system_move,
    file_system_remove,
    motion_snapshot,
    queue_maintenance,
)


class BooleanScenario(NamedTuple):
  exists: bool
  expected: bool


class MutableBooleanScenario(NamedTuple):
  side_effect: Tuple[bool, bool]
  expected: bool


@pytest.fixture
def mocked_chat_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_chat_file_task() -> mock.Mock:
  mock_task = mock.Mock()
  mock_task.args.path = "/mock/path.mp4"
  mock_task.on_failure = []
  mock_task.on_success = []
  return mock_task


@pytest.fixture
def mocked_chat_message_task() -> mock.Mock:
  mock_task = mock.Mock()
  mock_task.args.message = "Test message!"
  mock_task.on_failure = []
  mock_task.on_success = []
  return mock_task


@pytest.fixture
def mocked_file_system_move() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_system_path_task() -> mock.Mock:
  mock_task = mock.Mock()
  mock_task.args.path = "/mock/path.mp4"
  mock_task.on_failure = []
  mock_task.on_success = []
  return mock_task


@pytest.fixture
def mocked_file_system_src_dst_task() -> mock.Mock:
  mock_task = mock.Mock()
  mock_task.args.source = "/mock1/path.mp4"
  mock_task.args.destination = "/mock2/path.mp4"
  mock_task.on_failure = []
  mock_task.on_success = []
  return mock_task


@pytest.fixture
def mocked_file_system_remove() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_motion_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_motion_snapshot_task() -> mock.Mock:
  mock_task = mock.Mock()
  mock_task.args.camera = 2
  mock_task.on_failure = []
  mock_task.on_success = []
  return mock_task


@pytest.fixture
def mocked_os_path_exists() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_remove() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os(
    mocked_os_path_exists: mock.Mock,
    mocked_os_remove: mock.Mock,
) -> mock.Mock:
  instance = mock.Mock()
  instance.path.exists = mocked_os_path_exists
  instance.remove = mocked_os_remove
  return instance


@pytest.fixture
def mocked_queue_no_args_task() -> mock.Mock:
  mock_task = mock.Mock()
  mock_task.on_failure = []
  mock_task.on_success = []
  return mock_task


@pytest.fixture
def mocked_recover() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def setup_chat_processor_mocks(
    mocked_chat_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        chat_client.__name__ + ".ChatClientMixin.chat_client_class",
        mocked_chat_client,
    )

  return setup


@pytest.fixture
def archive_logs_task_processor_instance(
    mocked_task_logger: logging.Logger
) -> archive_logs.ProcessorClass:
  return archive_logs.ProcessorClass(mocked_task_logger)


@pytest.fixture
def archive_videos_task_processor_instance(
    mocked_task_logger: logging.Logger
) -> archive_videos.ProcessorClass:
  return archive_videos.ProcessorClass(mocked_task_logger)


@pytest.fixture
def chat_send_message_instance(
    mocked_task_logger: logging.Logger,
    setup_chat_processor_mocks: Callable[[], None],
) -> chat_send_message.ProcessorClass:
  setup_chat_processor_mocks()
  return chat_send_message.ProcessorClass(mocked_task_logger)


@pytest.fixture
def chat_upload_snapshot_instance(
    mocked_file_system_remove: mock.Mock,
    mocked_os: mock.Mock,
    mocked_recover: mock.Mock,
    mocked_task_logger: logging.Logger,
    setup_chat_processor_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> chat_upload_snapshot.ProcessorClass:
  monkeypatch.setattr(
      chat_upload_snapshot.__name__ + ".file_system_remove",
      mocked_file_system_remove,
  )
  monkeypatch.setattr(
      chat_upload_snapshot.__name__ + ".os",
      mocked_os,
  )
  monkeypatch.setattr(
      processor_base.__name__ + ".TaskProcessorBase.recover",
      mocked_recover,
  )
  setup_chat_processor_mocks()
  return chat_upload_snapshot.ProcessorClass(mocked_task_logger)


@pytest.fixture
def chat_upload_video_instance(
    mocked_file_system_move: mock.Mock,
    mocked_os_path_exists: mock.Mock,
    mocked_recover: mock.Mock,
    mocked_task_logger: logging.Logger,
    setup_chat_processor_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> chat_upload_video.ProcessorClass:
  monkeypatch.setattr(
      chat_upload_video.__name__ + ".file_system_move",
      mocked_file_system_move,
  )
  monkeypatch.setattr(
      chat_upload_video.__name__ + ".os.path.exists",
      mocked_os_path_exists,
  )
  monkeypatch.setattr(
      processor_base.__name__ + ".TaskProcessorBase.recover",
      mocked_recover,
  )
  setup_chat_processor_mocks()
  return chat_upload_video.ProcessorClass(mocked_task_logger)


@pytest.fixture
def file_system_copy_instance(
    mocked_shutil: mock.Mock,
    mocked_task_logger: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
) -> file_system_copy.ProcessorClass:
  monkeypatch.setattr(
      file_system_copy.__name__ + ".shutil",
      mocked_shutil,
  )
  return file_system_copy.ProcessorClass(mocked_task_logger)


@pytest.fixture
def file_system_move_instance(
    mocked_os: mock.Mock,
    mocked_recover: mock.Mock,
    mocked_shutil: mock.Mock,
    mocked_task_logger: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
) -> file_system_move.ProcessorClass:
  monkeypatch.setattr(
      file_system_move.__name__ + ".os",
      mocked_os,
  )
  monkeypatch.setattr(
      processor_base.__name__ + ".TaskProcessorBase.recover",
      mocked_recover,
  )
  monkeypatch.setattr(
      file_system_move.__name__ + ".shutil",
      mocked_shutil,
  )
  return file_system_move.ProcessorClass(mocked_task_logger)


@pytest.fixture
def file_system_remove_instance(
    mocked_os: mock.Mock,
    mocked_recover: mock.Mock,
    mocked_task_logger: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
) -> file_system_remove.ProcessorClass:
  monkeypatch.setattr(
      file_system_remove.__name__ + ".os",
      mocked_os,
  )
  monkeypatch.setattr(
      processor_base.__name__ + ".TaskProcessorBase.recover",
      mocked_recover,
  )
  return file_system_remove.ProcessorClass(mocked_task_logger)


@pytest.fixture
def motion_snapshot_instance(
    mocked_motion_client: mock.Mock,
    mocked_recover: mock.Mock,
    mocked_task_logger: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
) -> motion_snapshot.ProcessorClass:
  monkeypatch.setattr(
      motion_snapshot.__name__ + ".MotionClient",
      mocked_motion_client,
  )
  monkeypatch.setattr(
      processor_base.__name__ + ".TaskProcessorBase.recover",
      mocked_recover,
  )
  return motion_snapshot.ProcessorClass(mocked_task_logger)


@pytest.fixture
def queue_maintenance_instance(
    mocked_task_router: mock.Mock,
    mocked_task_logger: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
) -> queue_maintenance.ProcessorClass:
  monkeypatch.setattr(
      queue_maintenance.__name__ + ".TaskRouter",
      mocked_task_router,
  )
  queue_formatter = logging.Formatter(
      '%(levelname)s - %(task)s - %(queue)s - %(message)s',
      validate=False,
  )
  mocked_task_logger.handlers[0].formatter = queue_formatter
  return queue_maintenance.ProcessorClass(mocked_task_logger)
