"""Test the GPIOInputBase class."""

from .fixtures import concrete_input, input_harness


class TestGPIOInput(input_harness.GPIOInputTestHarness):
  """Test the GPIOInputBase class with a concrete implementation."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = concrete_input.ConcreteGPIOInput

  def test_poll(self) -> None:
    self.instance.poll()
    self.assertEqual(self.instance.last_state, self.gpio_input_1_initial_value)
    self.assertEqual(
        self.instance.current_state, self.gpio_input_1_initial_value + 1
    )
