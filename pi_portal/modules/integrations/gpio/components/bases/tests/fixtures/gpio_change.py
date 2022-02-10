"""Test helper to control the has_changed method on GPIOInputBase."""

from contextlib import ExitStack, contextmanager
from typing import Generator, List, Sequence
from unittest import mock

from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input


@contextmanager
def patch_gpio_input_change(
    gpio_pins: Sequence[gpio_input.GPIOInputBase], response: bool
) -> Generator[List[mock.MagicMock], None, None]:
  """Patch a list of GPIO inputs to force enable/disable state change detection.

  :param gpio_pins: A list of GPIOInputBase subclasses to patch.
  :param response: The mocked boolean value.
  :yields: A list of patched_mocks as a context manager.
  """

  with ExitStack() as stack:
    patched_mocks = []
    for gpio_pin in gpio_pins:
      patched_mocks.append(
          stack.enter_context(
              mock.patch.object(gpio_pin, "has_changed", return_value=response)
          )
      )
    yield patched_mocks
