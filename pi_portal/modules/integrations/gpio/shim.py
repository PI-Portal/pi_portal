"""Raspberry PI GPIO compatibility shim."""

import os
import sys
from importlib import import_module
from types import ModuleType
from unittest import mock


class IncompatiblePlatform(Exception):
  """Raised when accessing GPIO utilities on a non-compatible device."""


def patch_gpio() -> None:
  """Patch the GPIO library for testing on non-arm platforms."""

  if os.uname()[4][:3] != 'arm':
    try:
      import fake_rpi  # pylint: disable=import-error,import-outside-toplevel
      sys.modules['RPi'] = fake_rpi.RPi
      sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
    except ModuleNotFoundError:
      raise IncompatiblePlatform(  # pylint: disable=raise-missing-from
          "This application is designed to be run on a Raspberry Pi."
      )


def import_or_mock(module_name: str) -> ModuleType:
  """Patch the Adafruit libraries for testing on non-arm platforms."""

  try:
    if os.uname()[4][:3] == 'arm':
      return import_module(module_name)
  except NotImplementedError:
    pass

  if module_name not in sys.modules:
    sys.modules[module_name] = mock.MagicMock()
  return sys.modules[module_name]


patch_gpio()

adafruit_dht = import_or_mock("adafruit_dht")
board = import_or_mock("board")
import RPi.GPIO  # isort: skip pylint: disable=import-error,wrong-import-position,unused-import
