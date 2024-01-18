"""Utilities for working with futures."""

from concurrent.futures import Future
from contextlib import contextmanager
from typing import Any


@contextmanager
def wait_cm(future: "Future") -> Any:
  """Wait for a future to finish.

  :param future: The :class:`Future` to await.
  :yields: The future being awaited.
  :returns: The awaited future's result.
  """

  try:
    yield future
  finally:
    return future.result()  # pylint: disable=lost-exception
