"""Utilities for working with futures."""

from concurrent.futures import Future
from contextlib import contextmanager
from typing import Iterator, TypeVar

TypeAwaited = TypeVar("TypeAwaited")


@contextmanager
def wait_cm(future: "Future[TypeAwaited]") -> "Iterator[Future[TypeAwaited]]":
  """Wait for a future to finish.

  :param future: The :class:`Future` to await.
  :yields: The future being awaited.
  """

  try:
    yield future
  finally:
    future.result()
