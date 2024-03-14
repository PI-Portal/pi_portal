"""Test the StepBase class."""
import logging
from io import StringIO
from typing import List
from unittest import mock

from .. import base_step


class TestStepBase:
  """Test the StepBase class."""

  def test_initialize__attributes(
      self,
      concrete_base_step_instance: base_step.StepBase,
      mocked_actions: List[mock.Mock],
  ) -> None:
    assert isinstance(concrete_base_step_instance.log, logging.Logger)
    assert concrete_base_step_instance.actions == mocked_actions
    assert concrete_base_step_instance.logging_begin_message == (
        "mock begin message"
    )
    assert concrete_base_step_instance.logging_end_message == (
        "mock end message"
    )

  def test_invoke__logging(
      self,
      concrete_base_step_instance: base_step.StepBase,
      mocked_stream: StringIO,
  ) -> None:
    concrete_base_step_instance.invoke()

    assert mocked_stream.getvalue() == (
        f"INFO - {concrete_base_step_instance.logging_begin_message}\n"
        f"INFO - {concrete_base_step_instance.logging_end_message}\n"
    )

  def test_invoke__invokes_all_actions(
      self,
      concrete_base_step_instance: base_step.StepBase,
      mocked_actions: List[mock.Mock],
  ) -> None:
    concrete_base_step_instance.invoke()

    for mocked_action in mocked_actions:
      mocked_action.assert_called_once_with(concrete_base_step_instance.log)
      mocked_action.return_value.invoke.assert_called_once_with()
