"""Test fixtures for the commands mixins tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import state


@pytest.fixture
def mocked_state() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def command_managed_state_mixin_instance(
    mocked_state: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> state.CommandManagedStateMixin:
  monkeypatch.setattr(
      state.__name__ + ".state.State",
      mocked_state,
  )
  return state.CommandManagedStateMixin()
