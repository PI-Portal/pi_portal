"""Test the FileSystemRemoveProcessor class."""

import logging
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.file_system_remove import ProcessorClass
from .conftest import BooleanScenario


class TestFileSystemRemoveProcessor:
  """Test the FileSystemRemoveProcessor class."""

  def test_initialize__attributes(
      self,
      file_system_remove_instance: ProcessorClass,
  ) -> None:
    assert file_system_remove_instance.type == \
        TaskType.FILE_SYSTEM_REMOVE

  def test_initialize__logger(
      self,
      file_system_remove_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        file_system_remove_instance.log,
        logging.Logger,
    )
    assert file_system_remove_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      file_system_remove_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        file_system_remove_instance,
        processor_base.TaskProcessorBase,
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          BooleanScenario(exists=False, expected=True),
          BooleanScenario(exists=True, expected=False),
      ],
  )
  def test_process__recover(
      self,
      file_system_remove_instance: ProcessorClass,
      mocked_file_system_path_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_recover: mock.Mock,
      scenario: BooleanScenario,
  ) -> None:
    mocked_os_path_exists.return_value = scenario.exists

    file_system_remove_instance.process(mocked_file_system_path_task)

    called = mocked_recover.mock_calls == \
        [mock.call(mocked_file_system_path_task)]
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
  def test_process__os_remove(
      self,
      file_system_remove_instance: ProcessorClass,
      mocked_file_system_path_task: mock.Mock,
      mocked_os_path_exists: mock.Mock,
      mocked_os_remove: mock.Mock,
      scenario: BooleanScenario,
  ) -> None:
    mocked_os_path_exists.return_value = scenario.exists

    file_system_remove_instance.process(mocked_file_system_path_task)

    called = mocked_os_remove.mock_calls == \
        [mock.call(mocked_file_system_path_task.args.path)]
    not_called = mocked_os_remove.call_count == 0
    assert called is scenario.expected
    assert not_called is not scenario.expected
