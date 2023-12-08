"""A Supervisord client over a unix socket."""

import xmlrpc.client
from typing import cast

from pi_portal import config
from pi_portal.modules.system.socket import UnixStreamTransport
from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from typing_extensions import TypedDict


class SupervisorException(Exception):
  """Exceptions for the SupervisorClient class."""


class TypeSupervisorProcessInfo(TypedDict):
  """Typed representation of a Supervisor getProcessInfo response."""

  statename: ProcessStatus
  start: str


class SupervisorClient:
  """A Supervisor client that connects via the local unix socket.

  :param host: Unused, instead the transport uses a unix socket.
  :param port: Unused, instead the transport uses a unix socket.
  """

  def __init__(self, host: str = 'localhost', port: int = 9001):
    self.server = xmlrpc.client.Server(
        f"http://{host}:{port}",
        transport=UnixStreamTransport(config.PATH_SUPERVISOR_SOCKET)
    )

  def start(self, process: ProcessList) -> None:
    """Start the specified Supervisor process.

    :param process: The process to start.
    :raises: :class:`SupervisorException`
    """

    try:
      self.server.supervisor.startProcess(process.value)
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def stop(self, process: ProcessList) -> None:
    """Stop the specified Supervisor process.

    :param process: The process to stop.
    :raises: :class:`SupervisorException`
    """

    try:
      self.server.supervisor.stopProcess(process.value)
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def status(self, process: ProcessList) -> ProcessStatus:
    """Retrieve the current state of the specified Supervisor process.

    :param process: The process to retrieve the status of.
    :returns: The status of the queried process.
    :raises: :class:`SupervisorException`
    """
    try:
      return ProcessStatus(
          cast(
              TypeSupervisorProcessInfo,
              self.server.supervisor.getProcessInfo(process.value)
          )['statename']
      )
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def start_time(self, process: ProcessList) -> str:
    """Retrieve the start time of the specified Supervisor process.

    :param process: The process to retrieve the uptime of.
    :returns: The uptime of the queried process.
    :raises: :class:`SupervisorException`
    """

    try:
      return cast(
          TypeSupervisorProcessInfo,
          self.server.supervisor.getProcessInfo(process.value),
      )['start']
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc
