"""Shared test fixtures for the task queue modules."""

import logging

import pytest


@pytest.fixture
def mocked_queue_logger(mocked_task_logger: logging.Logger,) -> logging.Logger:
  worker_formatter = logging.Formatter(
      '%(levelname)s - %(task_id)s - %(task_type)s - %(queue)s - %(message)s',
      validate=False,
  )
  mocked_task_logger.handlers[0].formatter = worker_formatter
  return mocked_task_logger
