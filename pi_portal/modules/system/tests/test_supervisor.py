"""Test Supervisor SlackClient Class."""

import xmlrpc.client
from unittest import TestCase, mock

from pi_portal.modules.system import supervisor, supervisor_config


class TestSupervisorClient(TestCase):
  """Test the SupervisorClient class."""

  def setUp(self):
    self.supervisor_client = supervisor.SupervisorClient()
    self.supervisor_client.server = mock.MagicMock()

  def test_initialize(self):
    client = supervisor.SupervisorClient()
    self.assertIsInstance(client.server, xmlrpc.client.Server)

  def test_start(self):
    self.supervisor_client.start(supervisor_config.ProcessList.CAMERA)
    self.supervisor_client.server.supervisor.startProcess.\
      assert_called_once_with(
        supervisor_config.ProcessList.CAMERA.value
      )

  def test_start_error(self):
    self.supervisor_client.server.supervisor.startProcess.side_effect = (
        xmlrpc.client.Fault(1, "MockFaultError")
    )
    with self.assertRaises(supervisor.SupervisorException):
      self.supervisor_client.start(supervisor_config.ProcessList.CAMERA)

  def test_stop(self):
    self.supervisor_client.stop(supervisor_config.ProcessList.CAMERA)
    self.supervisor_client.server.supervisor.stopProcess.\
      assert_called_once_with(
        supervisor_config.ProcessList.CAMERA.value
      )

  def test_stop_error(self):
    self.supervisor_client.server.supervisor.stopProcess.side_effect = (
        xmlrpc.client.Fault(1, "MockFaultError")
    )
    with self.assertRaises(supervisor.SupervisorException):
      self.supervisor_client.stop(supervisor_config.ProcessList.CAMERA)

  def test_status(self):
    self.supervisor_client.status(supervisor_config.ProcessList.CAMERA)
    self.supervisor_client.server.supervisor.getProcessInfo.\
      assert_called_once_with(
        supervisor_config.ProcessList.CAMERA.value
      )

  def test_status_error(self):
    self.supervisor_client.server.supervisor.getProcessInfo.side_effect = (
        xmlrpc.client.Fault(1, "MockFaultError")
    )
    with self.assertRaises(supervisor.SupervisorException):
      self.supervisor_client.status(supervisor_config.ProcessList.CAMERA)

  def test_uptime(self):
    self.supervisor_client.uptime(supervisor_config.ProcessList.MONITOR)
    self.supervisor_client.server.supervisor.getProcessInfo.\
      assert_called_once_with(
        supervisor_config.ProcessList.MONITOR.value
      )

  def test_uptime_error(self):
    self.supervisor_client.server.supervisor.getProcessInfo.side_effect = (
        xmlrpc.client.Fault(1, "MockFaultError")
    )
    with self.assertRaises(supervisor.SupervisorException):
      self.supervisor_client.uptime(supervisor_config.ProcessList.MONITOR)
