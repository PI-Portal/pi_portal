"""GPIO input test harness."""

import abc
from typing import Any, Type
from unittest import TestCase, mock

from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input


class GPIOInputTestHarness(TestCase, abc.ABC):
  """Test harness for the GPIOInputBase class."""

  __test__ = False
  gpio_input_1_name = "test_pin_1"
  gpio_input_1_pin = 1
  gpio_input_1_initial_value: Any = 1
  test_class: Type[gpio_input.GPIOInputBase]

  def setUp(self) -> None:
    self.instance = self.test_class(
        pin_number=self.gpio_input_1_pin,
        pin_name=self.gpio_input_1_name,
        initial_state=self.gpio_input_1_initial_value,
    )

  def get_instance(self) -> gpio_input.GPIOInputBase:
    return self.instance

  def test_initialize(self) -> None:
    self.assertEqual(self.get_instance().pin_name, self.gpio_input_1_name)
    self.assertEqual(self.get_instance().pin_number, self.gpio_input_1_pin)
    self.assertEqual(
        self.get_instance().current_state, self.gpio_input_1_initial_value
    )
    self.assertIsNone(self.get_instance().last_state)

  def test_setup_input(self) -> None:
    with mock.patch.object(self.test_class, "hook_setup_input") as m_hook:
      self.setUp()
    m_hook.assert_called_once_with()

  def test_has_changed_false(self) -> None:
    self.get_instance().last_state = self.gpio_input_1_initial_value
    with mock.patch.object(self.get_instance(), "hook_update_state") as m_hook:
      m_hook.return_value = self.gpio_input_1_initial_value
      self.get_instance().poll()
    self.assertFalse(self.get_instance().has_changed())

  def test_has_changed_true(self) -> None:
    self.get_instance().last_state = 1
    with mock.patch.object(self.get_instance(), "hook_update_state") as m_hook:
      m_hook.return_value = 0
      self.get_instance().poll()
    self.assertTrue(self.get_instance().has_changed())

  @abc.abstractmethod
  def test_poll(self) -> None:
    """Override to test the poll method."""
