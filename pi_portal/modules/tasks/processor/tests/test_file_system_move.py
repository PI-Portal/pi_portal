"""Test the FileSystemMoveProcessor class."""

import logging
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.file_system_move import ProcessorClass
from .conftest import BooleanScenario


class TestFileSystemMoveProcessor:
  """Test the FileSystemMoveProcessor class."""

  def test_initialize__attributes(
      self,
      file_system_move_instance: ProcessorClass,
  ) -> None:
    assert file_system_move_instance.type == \
        TaskType.FILE_SYSTEM_MOVE

  def test_initialize__logger(
      self,
      file_system_move_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        file_system_move_instance.log,
        logging.Logger,
    )
    assert file_system_move_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      file_system_move_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        file_system_move_instance,
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
      file_system_move_instance: ProcessorClass,
      mocked_file_system_src_dst_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_recover: mock.Mock,
      scenario: BooleanScenario,
  ) -> None:
    mocked_os_path_exists.return_value = scenario.exists

    file_system_move_instance.process(mocked_file_system_src_dst_task)

    called = mocked_recover.mock_calls == \
        [mock.call(mocked_file_system_src_dst_task)]
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
  def test_process__vary_exists__calls_shutil(
      self,
      file_system_move_instance: ProcessorClass,
      mocked_file_system_src_dst_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_shutil: mock.Mock,
      scenario: BooleanScenario,
  ) -> None:
    mocked_os_path_exists.return_value = scenario.exists

    file_system_move_instance.process(mocked_file_system_src_dst_task)

    called = mocked_shutil.move.mock_calls == [
        mock.call(
            src=mocked_file_system_src_dst_task.args.source,
            dst=mocked_file_system_src_dst_task.args.destination,
        )
    ]
    not_called = mocked_shutil.move.call_count == 0
    assert called is scenario.expected
    assert not_called is not scenario.expected
