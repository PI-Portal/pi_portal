"""GPIO input test harness."""

import abc
from typing import Type
from unittest import TestCase, mock

from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input


class GPIOInputTestHarness(TestCase, abc.ABC):
  """Test harness for the GPIOInputBase class."""

  __test__ = False
  gpio_input_1_name = "test_pin_1"
  gpio_input_1_pin = 1
  gpio_input_1_initial_value = 1
  test_class: Type[gpio_input.GPIOInputBase]

  def setUp(self) -> None:
    self.instance = self.test_class(
        pin_number=self.gpio_input_1_pin,
        pin_name=self.gpio_input_1_name,
        initial_state=self.gpio_input_1_initial_value,
    )

  def test_initialize(self) -> None:
    self.assertEqual(self.instance.pin_name, self.gpio_input_1_name)
    self.assertEqual(self.instance.pin_number, self.gpio_input_1_pin)
    self.assertEqual(
        self.instance.current_state, self.gpio_input_1_initial_value
    )
    self.assertIsNone(self.instance.last_state)

  def test_has_changed_false(self) -> None:
    self.instance.last_state = 1
    with mock.patch.object(self.instance, "hook_update_state") as m_hook:
      m_hook.return_value = 1
      self.instance.poll()
    self.assertFalse(self.instance.has_changed())

  def test_has_changed_true(self) -> None:
    self.instance.last_state = 1
    with mock.patch.object(self.instance, "hook_update_state") as m_hook:
      m_hook.return_value = 0
      self.instance.poll()
    self.assertTrue(self.instance.has_changed())

  @abc.abstractmethod
  def test_poll(self) -> None:
    """Override to test the poll method."""
