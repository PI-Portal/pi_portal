"""Test fixtures for the configuration tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import state, user_config


@pytest.fixture
def mocked_user_configuration() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def state_instance(
    mocked_user_configuration: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> state.State:
  monkeypatch.setattr(
      state.__name__ + ".UserConfiguration",
      mocked_user_configuration,
  )
  return state.State()


@pytest.fixture
def state_instance_clone(
    mocked_user_configuration: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> state.State:
  monkeypatch.setattr(
      state.__name__ + ".UserConfiguration",
      mocked_user_configuration,
  )
  return state.State()


@pytest.fixture
def user_configuration_instance() -> user_config.UserConfiguration:
  return user_config.UserConfiguration()
