"""Fixtures for the steps modules base class tests."""
# pylint: disable=redefined-outer-name

import logging
from typing import List, Type, cast
from unittest import mock

import pytest
from pi_portal.installation.actions.bases import base_action
from .. import base_step


@pytest.fixture
def mocked_actions() -> List[mock.Mock]:
  return [
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
  ]


@pytest.fixture
def concrete_base_step_class(
    mocked_actions: List[mock.Mock],
) -> Type[base_step.StepBase]:

  class ConcreteBaseStep(base_step.StepBase):
    actions = cast(List[Type[base_action.ActionBase]], mocked_actions)
    logging_begin_message = "mock begin message"
    logging_end_message = "mock end message"

  return ConcreteBaseStep


@pytest.fixture
def concrete_base_step_instance(
    concrete_base_step_class: Type[base_step.StepBase],
    installer_logger_stdout: logging.Logger,
) -> base_step.StepBase:
  return concrete_base_step_class(installer_logger_stdout)
