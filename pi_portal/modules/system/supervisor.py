"""A Supervisord client over a unix socket."""

import xmlrpc.client
from typing import Dict, cast

from pi_portal import config
from pi_portal.modules.system.socket import UnixStreamTransport
from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)


class SupervisorException(Exception):
  """Exceptions for the Supervisor SlackClient."""


class SupervisorClient:
  """A Supervisor client that connects via the local unix socket."""

  def __init__(self, host: str = 'localhost', port: int = 9001):
    self.server = xmlrpc.client.Server(
        f"http://{host}:{port}",
        transport=UnixStreamTransport(config.SUPERVISOR_SOCKET_PATH)
    )

  def start(self, process: ProcessList):
    """Start the specified supervisor process.

    :param process: The process to start.
    """

    try:
      self.server.supervisor.startProcess(process.value)
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def stop(self, process: ProcessList):
    """Stop the specified supervisor process.

    :param process: The process to stop.
    """

    try:
      self.server.supervisor.stopProcess(process.value)
      return True
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def status(self, process: ProcessList) -> ProcessStatus:
    """Retrieve the current state of the specified supervisor process.

    :param process: The process to retrieve the status of.
    :return: The status of the queried process.
    """

    try:
      return cast(
          Dict,
          self.server.supervisor.getProcessInfo(process.value),
      )['statename']
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def uptime(self, process: ProcessList) -> str:
    """Retrieve the uptime the specified supervisor process.

    :param process: The process to retrieve the uptime of.
    :return: The uptime of the queried process.
    """

    try:
      return cast(
          Dict,
          self.server.supervisor.getProcessInfo(process.value),
      )['start']
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc
