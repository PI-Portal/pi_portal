"""Test the TaskProcessorBase class."""

from dataclasses import asdict
from datetime import datetime
from io import StringIO
from unittest import mock

from pi_portal.modules.python import traceback
from pi_portal.modules.tasks.enums import TaskType
from .conftest import TypeConcreteProcessor


class TestTaskProcessorBase:
  """Test the TaskProcessorBase class."""

  def test_initialize__attributes(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
  ) -> None:
    assert concrete_task_processor_base_instance.type == TaskType.BASE

  def test_process__success__logging(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_stream: StringIO,
      mocked_task: mock.Mock,
  ) -> None:
    concrete_task_processor_base_instance.process(mocked_task)

    assert mocked_stream.getvalue() == (
        f"DEBUG - {mocked_task.id} - Processing '{mocked_task}' ...\n"
        f"DEBUG - {mocked_task.id} - Completed '{mocked_task}'!\n"
    )

  def test_process__success__updates_task(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_task: mock.Mock,
      mocked_task_processor_implementation: mock.Mock,
  ) -> None:
    concrete_task_processor_base_instance.process(mocked_task)

    assert isinstance(mocked_task.completed, datetime)
    assert mocked_task.ok is True
    assert mocked_task.result == sum(asdict(mocked_task.args).values())
    mocked_task_processor_implementation.assert_called_once_with(mocked_task)

  def test_process__success__underlying_implementation(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_task: mock.Mock,
      mocked_task_processor_implementation: mock.Mock,
  ) -> None:
    concrete_task_processor_base_instance.process(mocked_task)

    mocked_task_processor_implementation.assert_called_once_with(mocked_task)

  def test_process__failure__logging(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_stream: StringIO,
      mocked_task: mock.Mock,
      mocked_task_processor_implementation: mock.Mock,
  ) -> None:
    mocked_task_processor_implementation.side_effect = Exception

    concrete_task_processor_base_instance.process(mocked_task)

    assert mocked_stream.getvalue() == (
        f"DEBUG - {mocked_task.id} - Processing '{mocked_task}' ...\n"
        f"ERROR - {mocked_task.id} - Failed: '{mocked_task}'!\n"
        f"ERROR - {mocked_task.id} - Exception\n" +
        traceback.get_traceback(mocked_task.result)
    )

  def test_process__failure__updates_task(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_task: mock.Mock,
      mocked_task_processor_implementation: mock.Mock,
  ) -> None:
    exception_instance = Exception("Specific Exception Instance")
    mocked_task_processor_implementation.side_effect = exception_instance

    concrete_task_processor_base_instance.process(mocked_task)

    assert isinstance(mocked_task.completed, datetime)
    assert mocked_task.result == exception_instance
    assert mocked_task.ok is False

  def test_process__failure__underlying_implementation(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_task: mock.Mock,
      mocked_task_processor_implementation: mock.Mock,
  ) -> None:
    mocked_task_processor_implementation.side_effect = Exception

    concrete_task_processor_base_instance.process(mocked_task)

    mocked_task_processor_implementation.assert_called_once_with(mocked_task)

  def test_recover__logging(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_stream: StringIO,
      mocked_task: mock.Mock,
  ) -> None:
    concrete_task_processor_base_instance.recover(mocked_task)

    assert mocked_stream.getvalue() == (
        f"WARNING - {mocked_task.id} - Recovered partially finished "
        f"'{mocked_task}'!\n"
    )
