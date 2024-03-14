"""Fixtures for the steps modules base class tests."""
# pylint: disable=redefined-outer-name

import logging
from typing import Type
from unittest import mock

import pytest
from .. import base_action, base_system_call_action


@pytest.fixture
def mocked_os_system() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_action_base_class() -> Type[base_action.ActionBase]:

  class ConcreteAction(base_action.ActionBase):

    def invoke(self) -> None:
      raise NotImplementedError  # pragma: no cover

  return ConcreteAction


@pytest.fixture
def concrete_action_base_instance(
    concrete_action_base_class: Type[base_action.ActionBase],
    installer_logger_stdout: logging.Logger,
) -> base_action.ActionBase:
  return concrete_action_base_class(installer_logger_stdout)


@pytest.fixture
def concrete_action_system_call_base_class(
    mocked_os_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[base_system_call_action.SystemCallActionBase]:
  monkeypatch.setattr(
      base_system_call_action.__name__ + ".os.system",
      mocked_os_system,
  )

  class ConcreteSystemCallAction(base_system_call_action.SystemCallActionBase):

    def invoke(self) -> None:
      raise NotImplementedError  # pragma: no cover

  return ConcreteSystemCallAction


@pytest.fixture
def concrete_action_system_call_base_instance(
    concrete_action_system_call_base_class: Type[
        base_system_call_action.SystemCallActionBase],
    installer_logger_stdout: logging.Logger,
) -> base_system_call_action.SystemCallActionBase:
  return concrete_action_system_call_base_class(installer_logger_stdout)
