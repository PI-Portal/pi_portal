"""Raspberry PI GPIO compatibility shim."""

import os
import sys


def patch_gpio() -> None:
  """Patch the GPIO library for testing on non-arm platforms."""

  if os.uname()[4][:3] != 'arm':
    try:
      import fake_rpi  # pylint: disable=import-error,import-outside-toplevel
      sys.modules['RPi'] = fake_rpi.RPi
      sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
    except ModuleNotFoundError:
      raise Exception(  # pylint: disable=raise-missing-from
          "This application is designed to be run on a Raspberry Pi."
      )


patch_gpio()
import RPi.GPIO  # isort: skip pylint: disable=import-error,wrong-import-position,unused-import
