"""Test the ChatUploadVideoProcessor class."""

import logging
import os
from io import StringIO
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.chat_upload_video import ProcessorClass
from pi_portal.modules.tasks.processor.mixins import chat_client
from .conftest import MutableBooleanScenario


class TestChatUploadVideoProcessor:
  """Test the ChatUploadVideoProcessor class."""

  def test_initialize__attributes(
      self,
      chat_upload_video_instance: ProcessorClass,
  ) -> None:
    assert chat_upload_video_instance.recovery_archival_suffix == "-RECOVERED"
    assert chat_upload_video_instance.type == TaskType.CHAT_UPLOAD_VIDEO

  def test_initialize__logger(
      self,
      chat_upload_video_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        chat_upload_video_instance.log,
        logging.Logger,
    )
    assert chat_upload_video_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      chat_upload_video_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        chat_upload_video_instance,
        chat_client.ChatClientMixin,
    )
    assert isinstance(
        chat_upload_video_instance,
        processor_base.TaskProcessorBase,
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          MutableBooleanScenario(side_effect=(False, False), expected=True),
          MutableBooleanScenario(side_effect=(False, True), expected=True),
          MutableBooleanScenario(side_effect=(True, False), expected=False),
          MutableBooleanScenario(side_effect=(True, True), expected=True),
      ],
  )
  def test_process__vary_src_dst_exists__calls_recover(
      self,
      chat_upload_video_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_recover: mock.Mock,
      scenario: MutableBooleanScenario,
  ) -> None:
    mocked_os_path_exists.side_effect = scenario.side_effect

    chat_upload_video_instance.process(mocked_chat_file_task)

    called = mocked_recover.mock_calls == [mock.call(mocked_chat_file_task)]
    not_called = mocked_recover.call_count == 0
    assert called is scenario.expected
    assert not_called is not scenario.expected

  @pytest.mark.parametrize(
      "scenario",
      [
          MutableBooleanScenario(side_effect=(False, False), expected=False),
          MutableBooleanScenario(side_effect=(False, True), expected=False),
          MutableBooleanScenario(side_effect=(True, False), expected=True),
          MutableBooleanScenario(side_effect=(True, True), expected=False),
      ],
  )
  def test_process__vary_src_dst_exists__calls_send_file(
      self,
      chat_upload_video_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_chat_client: mock.Mock,
      scenario: MutableBooleanScenario,
  ) -> None:
    mocked_os_path_exists.side_effect = scenario.side_effect
    mocked_send_file_call = mock.call(
        mocked_chat_file_task.args.path,
        mocked_chat_file_task.args.description,
    )

    chat_upload_video_instance.process(mocked_chat_file_task)

    called = mocked_chat_client.return_value.send_file.mock_calls == \
        [mocked_send_file_call]
    not_called = mocked_chat_client.return_value.send_file.call_count == 0
    assert called is scenario.expected
    assert not_called is not scenario.expected

  @pytest.mark.parametrize(
      "scenario",
      [
          MutableBooleanScenario(side_effect=(False, False), expected=False),
          MutableBooleanScenario(side_effect=(False, True), expected=False),
          MutableBooleanScenario(side_effect=(True, False), expected=True),
          MutableBooleanScenario(side_effect=(True, True), expected=False),
      ],
  )
  def test_process__vary_src_dst_exists__logging(
      self,
      chat_upload_video_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_stream: StringIO,
      scenario: MutableBooleanScenario,
  ) -> None:
    mocked_os_path_exists.side_effect = scenario.side_effect
    chat_video_task_id = mocked_chat_file_task.id
    chat_video_task_type = mocked_chat_file_task.type

    chat_upload_video_instance.process(mocked_chat_file_task)

    logging_with_upload = mocked_stream.getvalue() == (
        f"DEBUG - {chat_video_task_id} - {chat_video_task_type} - "
        f"Processing: '{mocked_chat_file_task}' ...\n"
        f"DEBUG - {chat_video_task_id} - {chat_video_task_type} - "
        f"Uploading: '{mocked_chat_file_task.args.path}' -> 'CHAT' ...\n"
        f"DEBUG - {chat_video_task_id} - {chat_video_task_type} - "
        f"Completed: '{mocked_chat_file_task}'!\n"
        f"DEBUG - {chat_video_task_id} - {chat_video_task_type} - "
        f"Task Timing: '{mocked_chat_file_task}'.\n"
    )
    logging_without_upload = mocked_stream.getvalue() == (
        f"DEBUG - {chat_video_task_id} - {chat_video_task_type} - "
        f"Processing: '{mocked_chat_file_task}' ...\n"
        f"DEBUG - {chat_video_task_id} - {chat_video_task_type} - "
        f"Completed: '{mocked_chat_file_task}'!\n"
        f"DEBUG - {chat_video_task_id} - {chat_video_task_type} - "
        f"Task Timing: '{mocked_chat_file_task}'.\n"
    )

    assert logging_with_upload is scenario.expected
    assert logging_without_upload is not scenario.expected

  @pytest.mark.parametrize(
      "scenario",
      [
          MutableBooleanScenario(side_effect=(False, False), expected=False),
          MutableBooleanScenario(side_effect=(False, True), expected=False),
          MutableBooleanScenario(side_effect=(True, False), expected=True),
          MutableBooleanScenario(side_effect=(True, True), expected=True),
      ],
  )
  def test_process__vary_src_dst_exists__creates_next_task(
      self,
      chat_upload_video_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_file_system_move_task_module: mock.Mock,
      scenario: MutableBooleanScenario,
  ) -> None:
    mocked_os_path_exists.side_effect = scenario.side_effect

    chat_upload_video_instance.process(mocked_chat_file_task)

    task_attached = (
        mocked_chat_file_task.on_success == [
            mocked_file_system_move_task_module.Task.return_value
        ]
    )
    no_next_task_created = not task_attached
    assert task_attached is scenario.expected
    assert no_next_task_created is not scenario.expected

  @pytest.mark.parametrize(
      "scenario",
      [
          MutableBooleanScenario(side_effect=(True, False), expected=True),
          MutableBooleanScenario(side_effect=(True, True), expected=False),
      ],
  )
  def test_process__vary_src_dst_exists__standard_filename_args(
      self,
      chat_upload_video_instance: ProcessorClass,
      mocked_chat_file_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_file_system_move_task_module: mock.Mock,
      scenario: MutableBooleanScenario,
  ) -> None:
    mocked_os_path_exists.side_effect = scenario.side_effect
    recovery_file_path = \
        f"path{chat_upload_video_instance.recovery_archival_suffix}.mp4"

    chat_upload_video_instance.process(mocked_chat_file_task)

    standard_args = (
        mocked_file_system_move_task_module.Args.mock_calls == [
            mock.call(
                source=mocked_chat_file_task.args.path,
                destination=os.path.join(
                    config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
                    os.path.basename(mocked_chat_file_task.args.path),
                )
            )
        ]
    )
    recovery_args = (
        mocked_file_system_move_task_module.Args.mock_calls == [
            mock.call(
                source=mocked_chat_file_task.args.path,
                destination=os.path.join(
                    config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
                    recovery_file_path,
                )
            )
        ]
    )
    assert standard_args is scenario.expected
    assert recovery_args is not scenario.expected
