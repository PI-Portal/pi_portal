"""Test the TaskProcessorBase class."""

from dataclasses import asdict
from datetime import datetime
from io import StringIO
from unittest import mock

import pytest
from pi_portal.modules.python import traceback
from pi_portal.modules.tasks.enums import TaskType
from .conftest import TimingScenario, TypeConcreteProcessor, TypeTimingSetup


class TestTaskProcessorBase:
  """Test the TaskProcessorBase class."""

  def test_initialize__attributes(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_task_router: mock.Mock,
  ) -> None:
    assert concrete_task_processor_base_instance.type == TaskType.BASE
    assert concrete_task_processor_base_instance.router == mocked_task_router

  @pytest.mark.parametrize(
      "scenario",
      [
          TimingScenario(
              creation_time=datetime(
                  year=2000, month=3, day=1, hour=11, minute=10
              ),
              completion_time=datetime(
                  year=2000, month=3, day=1, hour=11, minute=15
              ),
              processing_start_time=datetime(
                  year=2000, month=3, day=1, hour=11, minute=11
              ),
          ),
          TimingScenario(
              creation_time=datetime(
                  year=2000, month=3, day=1, hour=10, minute=10
              ),
              completion_time=datetime(
                  year=2000, month=3, day=1, hour=11, minute=15
              ),
              processing_start_time=datetime(
                  year=2000, month=3, day=1, hour=10, minute=30
              ),
          )
      ],
  )
  def test_log_timings__logging(
      self,
      concrete_task_processor_base_instance_with_timings: TypeConcreteProcessor,
      mocked_stream: StringIO,
      mocked_task: mock.Mock,
      scenario: TimingScenario,
      setup_task_timing: TypeTimingSetup,
  ) -> None:
    expected = setup_task_timing(scenario)

    concrete_task_processor_base_instance_with_timings.log_timings(
        scenario.processing_start_time,
        mocked_task,
    )

    assert mocked_stream.getvalue() == (
        f"DEBUG - {mocked_task.id} - Task Timing: '{mocked_task}'. - "
        f"{expected.processing_time} - "
        f"{expected.scheduled_time} - "
        f"{expected.total_time}\n"
    )

  def test_process__success__logging(
      self,
      concrete_task_processor_base_instance: TypeConcreteProcessor,
      mocked_stream: StringIO,
      mocked_task: mock.Mock,
  ) -> None:
    concrete_task_processor_base_instance.process(mocked_task)

    assert mocked_stream.getvalue() == (
        f"DEBUG - {mocked_task.id} - Processing: '{mocked_task}' ...\n"
        f"DEBUG - {mocked_task.id} - Completed: '{mocked_task}'!\n"
        f"DEBUG - {mocked_task.id} - Task Timing: '{mocked_task}'.\n"
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
    assert mocked_task.result.value == sum(asdict(mocked_task.args).values())
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
        f"DEBUG - {mocked_task.id} - Processing: '{mocked_task}' ...\n"
        f"ERROR - {mocked_task.id} - Failed: '{mocked_task}'!\n"
        f"ERROR - {mocked_task.id} - Exception\n" +
        traceback.get_traceback(mocked_task.result.value) +
        f"DEBUG - {mocked_task.id} - Task Timing: '{mocked_task}'.\n"
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
    assert mocked_task.result.value == exception_instance
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

    assert mocked_stream.getvalue() == \
        f"WARNING - {mocked_task.id} - Recovered: '{mocked_task}'!\n"
