"""Test the ContactSwitch class."""

from unittest import mock

from pi_portal.modules.integrations.gpio import shim
from pi_portal.modules.integrations.gpio.components import contact_switch
from ..bases.tests.fixtures import input_harness


class TestGPIOInput(input_harness.GPIOInputTestHarness):
  """Test the ContactSwitch class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = contact_switch.ContactSwitch

  def test_poll(self) -> None:
    with mock.patch(shim.__name__ + ".RPi.GPIO") as m_poll:
      m_poll.input.return_value = 1
      self.instance.poll()
    m_poll.input.assert_called_once_with(self.instance.pin_number)
    self.assertTrue(self.instance.current_state)

  def test_poll_false(self) -> None:
    with mock.patch(shim.__name__ + ".RPi.GPIO") as m_poll:
      m_poll.input.return_value = 0
      self.instance.poll()
    m_poll.input.assert_called_once_with(self.instance.pin_number)
    self.assertFalse(self.instance.current_state)
