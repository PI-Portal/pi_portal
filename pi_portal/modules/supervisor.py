"""A Supervisord client over a unix socket."""

import xmlrpc.client
from enum import Enum

from pi_portal import config
from pi_portal.modules.socket import UnixStreamTransport


class ProcessStatus(Enum):
  """Supervisor process states."""

  FATAL = 'FATAL'
  RESTARTING = 'RESTARTING'
  RUNNING = 'RUNNING'
  SHUTDOWN = 'SHUTDOWN'
  STOPPED = 'STOPPED'


class ProcessList(Enum):
  """Supervisor processes."""

  BOT = 'bot'
  CAMERA = 'camera'
  MONITOR = 'monitor'
  FILEBEAT = 'filebeat'


class SupervisorException(Exception):
  """Exceptions for the Supervisor Client."""


class SupervisorClient:
  """A Supervisor client that connects via the local unix socket."""

  def __init__(self, host='localhost', port=9001):
    self.server = xmlrpc.client.Server(
        f"http://{host}:{port}",
        transport=UnixStreamTransport(config.SUPERVISOR_SOCKET_PATH)
    )

  def start(self, process: ProcessList):
    """Start the specified supervisor process."""

    try:
      self.server.supervisor.startProcess(process.value)
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def stop(self, process: ProcessList):
    """Stop the specified supervisor process."""

    try:
      self.server.supervisor.stopProcess(process.value)
      return True
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def status(self, process: ProcessList) -> ProcessStatus:
    """Retrieve the current state of the specified supervisor process."""

    try:
      return self.server.supervisor.getProcessInfo(process.value)['statename']
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc

  def uptime(self, process: ProcessList) -> ProcessStatus:
    """Retrieve the uptime the specified supervisor process."""

    try:
      return self.server.supervisor.getProcessInfo(process.value)['start']
    except xmlrpc.client.Fault as exc:
      raise SupervisorException from exc
