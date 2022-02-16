"""SupervisorProcess class."""

from datetime import datetime
from typing import List

import humanize
from pi_portal.modules.system import supervisor, supervisor_config


class SupervisorProcessException(Exception):
  """Raised when a SupervisorProcess is unexpectedly in the wrong state."""


class SupervisorProcess:
  """Process managed by the SupervisorClient.

  :param process_name: The Supervisor process name.
  """

  uptime_when_stopped = "Not Running"

  def __init__(self, process_name: supervisor_config.ProcessList) -> None:
    self.client = supervisor.SupervisorClient()
    self.process_name = process_name

  def start(self) -> None:
    """Start the specified Supervisor process.

    :raises: :class:`SupervisorProcessException`
    """
    query = self.status_in(
        [
            supervisor_config.ProcessStatus.RUNNING,
            supervisor_config.ProcessStatus.RESTARTING,
        ]
    )
    if not query:
      self.client.start(self.process_name)
    else:
      raise SupervisorProcessException("Already Running.")

  def status(self) -> str:
    """Return the specified Supervisor process's status."""

    return self.client.status(self.process_name).value

  def status_in(self, status: List[supervisor_config.ProcessStatus]) -> bool:
    """Check if the Supervisor process is in the list of specified states.

    :param status: A list of statuses to check if the process is in.
    :returns: A boolean indicating if the process is one of the states.
    """
    query_status = self.client.status(self.process_name)
    return query_status.value in [check_status.value for check_status in status]

  def stop(self) -> None:
    """Stop the specified Supervisor process.

    :raises: :class:`SupervisorProcessException`
    """

    query = self.status_in(
        [
            supervisor_config.ProcessStatus.RUNNING,
            supervisor_config.ProcessStatus.RESTARTING,
        ]
    )
    if query:
      self.client.stop(self.process_name)
    else:
      raise SupervisorProcessException("Already Stopped.")

  def uptime(self) -> str:
    """Retrieve the uptime the specified Supervisor process.

    :returns: The uptime of the process.
    """

    if not self.status_in([supervisor_config.ProcessStatus.RUNNING]):
      return self.uptime_when_stopped
    uptime = datetime.now() - datetime.fromtimestamp(
        int(self.client.start_time(self.process_name))
    )
    return humanize.naturaldelta(uptime)
