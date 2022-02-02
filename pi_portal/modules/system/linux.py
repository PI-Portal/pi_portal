"""Linux utilities for the Pi Portal project."""

import time
from datetime import timedelta

import humanize


def uptime() -> str:
  """Report the system's uptime.

  :returns: The system's uptime as a naturalized string.
  """

  uptime_linux_seconds = time.monotonic()
  uptime_timedelta = timedelta(seconds=uptime_linux_seconds)
  return humanize.naturaldelta(uptime_timedelta)
