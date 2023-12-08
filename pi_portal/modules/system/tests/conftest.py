"""Test fixtures for the system modules tests."""
# pylint: disable=redefined-outer-name

import time
from unittest import mock

import pytest
from .. import process


@pytest.fixture
def mocked_sleep() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def pid_file_path() -> str:
  return '/var/run/motion/motion.pid'


@pytest.fixture
def process_instance(
    mocked_sleep: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
    pid_file_path: str,
) -> process.Process:
  monkeypatch.setattr(time, 'sleep', mocked_sleep)
  return process.Process(pid_file_path)
