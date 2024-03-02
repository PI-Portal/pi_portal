"""Test fixtures for the task scheduler api module tests."""
# pylint: disable=redefined-outer-name

import os
from dataclasses import asdict, dataclass
from typing import Any, Dict, List
from unittest import mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pi_portal import config
from pi_portal.modules.tasks import scheduler
from pi_portal.modules.tasks.registration import registry, registry_factory
from pi_portal.modules.tasks.task import (
    archive_logs,
    archive_videos,
    camera_snapshot,
    chat_send_message,
    chat_upload_snapshot,
    chat_upload_video,
    file_system_copy,
    file_system_move,
    file_system_remove,
    non_scheduled,
    queue_maintenance,
)
from pi_portal.modules.tasks.task.bases import task_args_base
from typing_extensions import NotRequired, TypedDict
from .. import lifespan, router, security, server


class TypedTaskCreationRequestParameters(TypedDict):
  type: str
  args: Dict[str, Any]
  retry_after: NotRequired[int]
  routing_label: NotRequired[str]
  on_failure: NotRequired[List["TypedTaskCreationRequestParameters"]]
  on_success: NotRequired[List["TypedTaskCreationRequestParameters"]]


@dataclass
class InvalidArg(task_args_base.TaskArgsBase):
  invalid_arg: str


enabled_tasks__valid_payloads__creation_request_scenarios = [
    TypedTaskCreationRequestParameters(
        type=camera_snapshot.TaskType.value,
        args=asdict(camera_snapshot.Args(camera=2)),
    ),
    TypedTaskCreationRequestParameters(
        type=chat_send_message.TaskType.value,
        args=asdict(chat_send_message.Args(message="Test message.")),
    ),
    TypedTaskCreationRequestParameters(
        type=chat_upload_snapshot.TaskType.value,
        args=asdict(
            chat_upload_snapshot.Args(
                description="A snapshot file for testing purposes.",
                path=os.path.join(
                    config.PATH_CAMERA_CONTENT,
                    "file1",
                )
            )
        ),
    ),
    TypedTaskCreationRequestParameters(
        type=chat_upload_video.TaskType.value,
        args=asdict(
            chat_upload_video.Args(
                description="A video file for testing purposes.",
                path=os.path.join(
                    config.PATH_CAMERA_CONTENT,
                    "file1",
                )
            )
        ),
    ),
    TypedTaskCreationRequestParameters(
        type=file_system_copy.TaskType.value,
        args=asdict(
            file_system_copy.Args(
                source=os.path.join(
                    config.LOG_FILE_BASE_FOLDER,
                    "file1",
                ),
                destination=os.path.join(
                    config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD,
                    "file1",
                ),
            )
        ),
    ),
]

enabled_tasks__invalid__payloads__creation_request_scenarios = [
    TypedTaskCreationRequestParameters(
        type=camera_snapshot.TaskType.value,
        args=asdict(InvalidArg(invalid_arg="invalid_args")),
    ),
    TypedTaskCreationRequestParameters(
        type=chat_send_message.TaskType.value,
        args=asdict(InvalidArg(invalid_arg="invalid_args")),
    ),
    TypedTaskCreationRequestParameters(
        type=chat_upload_snapshot.TaskType.value,
        args=asdict(InvalidArg(invalid_arg="invalid_args")),
    ),
    TypedTaskCreationRequestParameters(
        type=chat_upload_video.TaskType.value,
        args=asdict(InvalidArg(invalid_arg="invalid_args")),
    ),
    TypedTaskCreationRequestParameters(
        type=file_system_copy.TaskType.value,
        args=asdict(InvalidArg(invalid_arg="invalid_args")),
    ),
]

disabled_tasks__valid_payloads__creation_request_scenarios = [
    TypedTaskCreationRequestParameters(
        type=archive_logs.TaskType.value,
        args=asdict(archive_logs.Args(partition_name="partition1")),
    ),
    TypedTaskCreationRequestParameters(
        type=archive_videos.TaskType.value,
        args=asdict(archive_videos.Args(partition_name="partition2")),
    ),
    TypedTaskCreationRequestParameters(
        type=file_system_move.TaskType.value,
        args=asdict(
            file_system_move.Args(
                source=os.path.join(
                    config.PATH_CAMERA_CONTENT,
                    "file1",
                ),
                destination=os.path.join(
                    config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
                    "file1",
                ),
            )
        ),
    ),
    TypedTaskCreationRequestParameters(
        type=file_system_remove.TaskType.value,
        args=asdict(
            file_system_remove.Args(
                path=os.path.join(
                    config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
                    "file2",
                )
            )
        ),
    ),
    TypedTaskCreationRequestParameters(
        type=non_scheduled.TaskType.value,
        args=asdict(non_scheduled.Args()),
    ),
    TypedTaskCreationRequestParameters(
        type=queue_maintenance.TaskType.value,
        args=asdict(queue_maintenance.Args()),
    ),
]


@pytest.fixture
def mocked_fast_api() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_system(
    mocked_file_system_objects: List[mock.Mock],
) -> mock.Mock:
  instance = mock.Mock(side_effect=mocked_file_system_objects)
  return instance


@pytest.fixture
def mocked_file_system_objects() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def task_registry() -> registry.TaskRegistry:
  return registry_factory.RegistryFactory().create()


@pytest.fixture
def mocked_os_path_exists() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_queue() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_router_factory() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_scheduler(mocked_queue: mock.Mock) -> mock.Mock:
  instance = mock.Mock()
  instance.queue = mocked_queue
  return instance


@pytest.fixture
def mocked_sleep() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_socket_security() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_threadpool_executor() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def router_factory_instance(
    mocked_scheduler: mock.Mock
) -> router.RouterFactory:
  return router.RouterFactory(mocked_scheduler)


@pytest.fixture
def server_instance(
    mocked_scheduler: mock.Mock,
    mocked_router_factory: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> server.Server:
  monkeypatch.setattr(
      server.__name__ + ".FastAPI.include_router",
      mock.Mock(),
  )
  monkeypatch.setattr(
      server.__name__ + ".RouterFactory",
      mocked_router_factory,
  )
  return server.Server(mocked_scheduler)


@pytest.fixture
def server_instance_with_mocked_fast_api(
    mocked_fast_api: mock.Mock,
    mocked_router_factory: mock.Mock,
    mocked_scheduler: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> server.Server:
  monkeypatch.setattr(
      server.__name__ + ".FastAPI",
      mocked_fast_api,
  )
  monkeypatch.setattr(
      server.__name__ + ".RouterFactory",
      mocked_router_factory,
  )
  return server.Server(mocked_scheduler)


@pytest.fixture
def socket_security_instance(
    mocked_file_system: mock.Mock,
    mocked_os_path_exists: mock.Mock,
    mocked_sleep: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> security.SocketSecurity:
  monkeypatch.setattr(
      security.__name__ + ".FileSystem",
      mocked_file_system,
  )
  monkeypatch.setattr(
      security.__name__ + ".time.sleep",
      mocked_sleep,
  )
  monkeypatch.setattr(
      security.__name__ + ".os.path.exists",
      mocked_os_path_exists,
  )
  return security.SocketSecurity()


@pytest.fixture
def test_app(
    mocked_task_router: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> FastAPI:
  app = FastAPI()
  monkeypatch.setattr(
      scheduler.__name__ + ".TaskRouter",
      mocked_task_router,
  )
  scheduler_instance = scheduler.TaskScheduler()
  router_instance = router.RouterFactory(scheduler_instance).create()
  app.include_router(router_instance)
  return app


@pytest.fixture
def test_app_threads(
    server_instance: server.Server,
    mocked_socket_security: mock.Mock,
    mocked_threadpool_executor: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> FastAPI:
  monkeypatch.setattr(
      lifespan.__name__ + ".ThreadPoolExecutor",
      mocked_threadpool_executor,
  )
  monkeypatch.setattr(
      lifespan.__name__ + ".SocketSecurity",
      mocked_socket_security,
  )
  return server_instance.api


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
  return TestClient(test_app)


@pytest.fixture
def test_client_threads(test_app_threads: FastAPI) -> TestClient:
  return TestClient(test_app_threads)
