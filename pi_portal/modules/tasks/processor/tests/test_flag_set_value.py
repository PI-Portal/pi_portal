"""Test the FlagSetValueProcessor class."""

import logging
from io import StringIO
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.flag_set_value import ProcessorClass


class TestFlagSetValueProcessor:
  """Test the FlagSetValueProcessor class."""

  log_message = (
      "DEBUG - {task.id} - {task.type} - Processing: '{task}' ...\n"
      "DEBUG - {task.id} - {task.type} - Setting flag: "
      "'{task.args.flag_name}' -> '{task.args.value}' .\n"
      "DEBUG - {task.id} - {task.type} - Completed: '{task}'!\n"
      "DEBUG - {task.id} - {task.type} - Task Timing: '{task}'.\n"
  )

  def test_initialize__attributes(
      self,
      flag_set_value_instance: ProcessorClass,
  ) -> None:
    assert flag_set_value_instance.type == \
        TaskType.FLAG_SET_VALUE

  def test_initialize__logger(
      self,
      flag_set_value_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        flag_set_value_instance.log,
        logging.Logger,
    )
    assert flag_set_value_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      flag_set_value_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        flag_set_value_instance,
        processor_base.TaskProcessorBase,
    )

  @pytest.mark.parametrize("flag_value", [True, False])
  def test_process__vary_value__logging(
      self,
      flag_set_value_instance: ProcessorClass,
      mocked_base_task: mock.Mock,
      mocked_stream: StringIO,
      flag_value: bool,
  ) -> None:
    mocked_base_task.type = flag_set_value_instance.type
    mocked_base_task.args.flag_name = "FLAG_CAMERA_DISABLED_BY_CRON"
    mocked_base_task.args.value = flag_value

    flag_set_value_instance.process(mocked_base_task)

    assert mocked_stream.getvalue() == self.log_message.format(
        task=mocked_base_task
    )

  @pytest.mark.parametrize("flag_value", [True, False])
  def test_process__vary_value__sets_flag_value(
      self,
      flag_set_value_instance: ProcessorClass,
      mocked_base_task: mock.Mock,
      mocked_flags: mock.Mock,
      flag_value: bool,
  ) -> None:
    mocked_base_task.type = flag_set_value_instance.type
    mocked_base_task.args.flag_name = "FLAG_CAMERA_DISABLED_BY_CRON"
    mocked_base_task.args.value = flag_value

    flag_set_value_instance.process(mocked_base_task)

    assert getattr(
        mocked_flags,
        mocked_base_task.args.flag_name,
    ) == flag_value
