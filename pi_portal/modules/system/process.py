"""Manage pi_portal related processes."""

import os
import signal
import time
from typing import Optional, cast


class ProcessNotTerminating(Exception):
  """Raised when a process won't terminate."""


class Process:
  """A linux process managed by pi_portal.

  :param pid_file_location: The location of the process's PID file.
  """

  pid_file_path: str
  timeout_counter: int = 10
  timeout_interval: float = 0.1

  def __init__(self, pid_file_location: str) -> None:
    self.pid_file_path = pid_file_location

  def kill(self, sig: int = signal.SIGTERM) -> None:
    """Terminate the process with SIGTERM, then SIGKILL if necessary.

    :param sig: The signal to send to the process.
    """
    pid = self._get_pid()

    if self._is_alive(pid):
      try:
        os.kill(cast(int, pid), sig)
        self._wait_to_die(pid)
      except ProcessLookupError:
        pass
      except ProcessNotTerminating as exc:
        if sig == signal.SIGTERM:
          self.kill(sig=signal.SIGKILL)
        else:
          raise exc

  def _wait_to_die(self, pid: Optional[int]) -> None:
    counter = 0
    while self._is_alive(pid) and counter < self.timeout_counter:
      counter += 1
      time.sleep(self.timeout_interval)

    if counter == self.timeout_counter:
      raise ProcessNotTerminating

  def _get_pid(self) -> Optional[int]:
    try:
      with open(self.pid_file_path, 'r', encoding='utf-8') as pid_file:
        return int(pid_file.read())
    except FileNotFoundError:
      return None

  def _is_alive(self, pid: Optional[int]) -> bool:
    if pid:
      try:
        os.kill(pid, 0)
        return True
      except ProcessLookupError:
        pass
    return False
