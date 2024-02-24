"""Shared test fixtures for the GPIO monitor modules tests."""
# pylint: disable=redefined-outer-name

from io import StringIO
from typing import Callable, List
from unittest import mock

import pytest
from .bases import monitor_base


@pytest.fixture
def mocked_gpio_pins() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_rpi_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_chat_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_sleep() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def setup_monitor_mocks(
    monkeypatch: pytest.MonkeyPatch,
    mocked_rpi_module: mock.Mock,
    mocked_chat_client: mock.Mock,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        monitor_base.__name__ + ".RPi",
        mocked_rpi_module,
    )
    monkeypatch.setattr(
        monitor_base.__name__ + ".ChatClient",
        mocked_chat_client,
    )

  return setup
