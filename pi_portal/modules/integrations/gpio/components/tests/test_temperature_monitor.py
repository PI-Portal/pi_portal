"""Test the TemperatureSensorMonitor Class."""

from pi_portal.modules.integrations.gpio.components import temperature_monitor
from .. import dht11_sensor
from ..bases.tests.fixtures import monitor_harness


class TestDHTSensorMonitor(monitor_harness.GPIOMonitorTestHarness):
  """Test the TemperatureSensorMonitor class."""

  __test__ = True
  gpio_input_1 = dht11_sensor.DHT11(1, "test1")
  gpio_input_2 = dht11_sensor.DHT11(2, "test2")

  @classmethod
  def setUpClass(cls) -> None:

    class TestableSensor(temperature_monitor.TemperatureSensorMonitor):
      gpio_poll_interval = 0.01

    cls.test_class = TestableSensor

  def test_hook_log_state_with_fake_value(self) -> None:
    self.gpio_input_1.current_state = {
        "temperature": 22.0,
        "humidity": 15.0,
    }
    self.gpio_input_1.pin_name = "Kitchen"

    with self.assertLogs(self.instance.log, level='DEBUG') as logs:
      self.instance.hook_log_state(self.gpio_input_1)

    self.assertListEqual(
        logs.output, [
            f"INFO:{self.instance.logger_name}:"
            f"{self.instance.gpio_pins[0].pin_name}:"
            f"Temperature:{self.gpio_input_1.current_state['temperature']}",
            f"INFO:{self.instance.logger_name}:"
            f"{self.instance.gpio_pins[0].pin_name}:"
            f"Humidity:{self.gpio_input_1.current_state['humidity']}"
        ]
    )
