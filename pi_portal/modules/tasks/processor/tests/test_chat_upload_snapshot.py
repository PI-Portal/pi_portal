"""Test the ChatUploadSnapshotProcessor class."""

import logging
from io import StringIO
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.chat_upload_snapshot import (
    ProcessorClass,
)
from pi_portal.modules.tasks.processor.mixins import chat_client
from .conftest import BooleanScenario


class TestChatUploadSnapshotProcessor:
  """Test the ChatUploadSnapshotProcessor class."""

  def test_initialize__attributes(
      self,
      chat_upload_snapshot_instance: ProcessorClass,
  ) -> None:
    assert chat_upload_snapshot_instance.type == TaskType.CHAT_UPLOAD_SNAPSHOT

  def test_initialize__logger(
      self,
      chat_upload_snapshot_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        chat_upload_snapshot_instance.log,
        logging.Logger,
    )
    assert chat_upload_snapshot_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      chat_upload_snapshot_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        chat_upload_snapshot_instance,
        chat_client.ChatClientMixin,
    )
    assert isinstance(
        chat_upload_snapshot_instance,
        processor_base.TaskProcessorBase,
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          BooleanScenario(exists=False, expected=True),
          BooleanScenario(exists=True, expected=False),
      ],
  )
  def test_process__vary_exists__calls_recover(
      self,
      chat_upload_snapshot_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_recover: mock.Mock,
      scenario: BooleanScenario,
  ) -> None:
    mocked_os_path_exists.return_value = scenario.exists

    chat_upload_snapshot_instance.process(mocked_chat_file_task)

    called = mocked_recover.mock_calls == [mock.call(mocked_chat_file_task)]
    not_called = mocked_recover.call_count == 0
    assert called is scenario.expected
    assert not_called is not scenario.expected

  @pytest.mark.parametrize(
      "scenario",
      [
          BooleanScenario(exists=False, expected=False),
          BooleanScenario(exists=True, expected=True),
      ],
  )
  def test_process__vary_exists__calls_send_file(
      self,
      chat_upload_snapshot_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_chat_client: mock.Mock,
      scenario: BooleanScenario,
  ) -> None:
    mocked_os_path_exists.return_value = scenario.exists
    mocked_send_file_call = mock.call(
        mocked_chat_file_task.args.path,
        mocked_chat_file_task.args.description,
    )

    chat_upload_snapshot_instance.process(mocked_chat_file_task)

    called = mocked_chat_client.return_value.send_file.mock_calls == \
        [mocked_send_file_call]
    not_called = mocked_chat_client.return_value.send_file.call_count == 0
    assert called is scenario.expected
    assert not_called is not scenario.expected

  @pytest.mark.parametrize(
      "scenario",
      [
          BooleanScenario(exists=False, expected=False),
          BooleanScenario(exists=True, expected=True),
      ],
  )
  def test_process__vary_exists__logging(
      self,
      chat_upload_snapshot_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_stream: StringIO,
      scenario: BooleanScenario,
  ) -> None:
    mocked_os_path_exists.return_value = scenario.exists
    chat_snapshot_task_id = mocked_chat_file_task.id
    chat_snapshot_task_type = mocked_chat_file_task.type

    chat_upload_snapshot_instance.process(mocked_chat_file_task)

    logging_with_upload = mocked_stream.getvalue() == (
        f"DEBUG - {chat_snapshot_task_id} - {chat_snapshot_task_type} - "
        f"Processing: '{mocked_chat_file_task}' ...\n"
        f"DEBUG - {chat_snapshot_task_id} - {chat_snapshot_task_type} - "
        f"Uploading: '{mocked_chat_file_task.args.path}' -> 'CHAT' ...\n"
        f"DEBUG - {chat_snapshot_task_id} - {chat_snapshot_task_type} - "
        f"Completed: '{mocked_chat_file_task}'!\n"
        f"DEBUG - {chat_snapshot_task_id} - {chat_snapshot_task_type} - "
        f"Task Timing: '{mocked_chat_file_task}'.\n"
    )
    logging_without_upload = mocked_stream.getvalue() == (
        f"DEBUG - {chat_snapshot_task_id} - {chat_snapshot_task_type} - "
        f"Processing: '{mocked_chat_file_task}' ...\n"
        f"DEBUG - {chat_snapshot_task_id} - {chat_snapshot_task_type} - "
        f"Completed: '{mocked_chat_file_task}'!\n"
        f"DEBUG - {chat_snapshot_task_id} - {chat_snapshot_task_type} - "
        f"Task Timing: '{mocked_chat_file_task}'.\n"
    )

    assert logging_with_upload is scenario.exists
    assert logging_without_upload is not scenario.exists

  @pytest.mark.parametrize(
      "scenario",
      [
          BooleanScenario(exists=False, expected=False),
          BooleanScenario(exists=True, expected=True),
      ],
  )
  def test_process__vary_exists__creates_success_task(
      self,
      chat_upload_snapshot_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_file_system_remove_task_module: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      scenario: BooleanScenario,
  ) -> None:
    mocked_os_path_exists.return_value = scenario.exists

    chat_upload_snapshot_instance.process(mocked_chat_file_task)

    created = mocked_chat_file_task.on_success == \
        [mocked_file_system_remove_task_module.Task.return_value]
    args_created = (
        mocked_file_system_remove_task_module.Args.mock_calls == [
            mock.call(path=mocked_chat_file_task.args.path)
        ]
    )
    task_created = (
        mocked_file_system_remove_task_module.Task.mock_calls == [
            mock.call(
                args=mocked_file_system_remove_task_module.Args.return_value
            )
        ]
    )
    not_created = not created
    not_args_created = (
        mocked_file_system_remove_task_module.Args.call_count == 0
    )
    not_task_created = (
        mocked_file_system_remove_task_module.Task.call_count == 0
    )
    assert created is scenario.expected
    assert args_created is scenario.expected
    assert task_created is scenario.expected
    assert not_created is not scenario.expected
    assert not_args_created is not scenario.expected
    assert not_task_created is not scenario.expected
