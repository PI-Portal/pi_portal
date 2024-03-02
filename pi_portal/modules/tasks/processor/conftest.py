"""Shared test fixtures for the task processor modules."""

import datetime
from unittest import mock

import pytest


@pytest.fixture
def mocked_base_task() -> mock.Mock:
  utc_now = datetime.datetime.now(tz=datetime.timezone.utc)
  base_task = mock.Mock()
  base_task.created = utc_now - datetime.timedelta(hours=1)
  base_task.scheduled = utc_now - datetime.timedelta(minutes=30)
  base_task.on_failure = []
  base_task.on_success = []
  return base_task
