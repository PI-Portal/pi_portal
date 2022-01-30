"""Linux utilities for the Pi Portal project."""

from datetime import timedelta

import humanize


def uptime() -> str:
  """Report the system's uptime.

  :return: The system's uptime as a naturalized string.
  """

  with open('/proc/uptime', 'r', encoding='utf-8') as file_handle:
    uptime_linux_seconds = float(file_handle.readline().split()[0])
    uptime_string_seconds = timedelta(seconds=uptime_linux_seconds)
  return humanize.naturaldelta(uptime_string_seconds)
