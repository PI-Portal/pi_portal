"""Test the GPIOInputBase class."""

from types import LambdaType

from .fixtures import concrete_sensor, sensor_harness


class TestGPIOInput(sensor_harness.GPIOSensorTestHarness):
  """Test the GPIOInputBase class with a concrete implementation."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = concrete_sensor.ConcreteGPIOSensor

  def test_hook_setup_hardware(self) -> None:
    self.assertIsInstance(self.get_instance().hardware, LambdaType)

  def test_poll(self) -> None:
    self.assertEqual(
        self.instance.current_state,
        self.gpio_input_1_initial_value,
    )
    self.instance.poll()
    self.assertEqual(self.instance.last_state, self.gpio_input_1_initial_value)
    self.assertNotEqual(self.instance.current_state, self.instance.last_state)
    self.assertGreaterEqual(self.instance.current_state, 90)
    self.assertLessEqual(self.instance.current_state, 100)
