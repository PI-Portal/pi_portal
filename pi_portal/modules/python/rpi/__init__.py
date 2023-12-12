"""Raspberry PI GPIO compatibility shim."""

from .patch import patch_module

patch_module("adafruit_dht")
patch_module("board")
patch_module("RPi", substitute_module="fake_rpi.RPi")
patch_module("RPi.GPIO")

import adafruit_dht  # pylint: disable=wrong-import-position
import board  # pylint: disable=wrong-import-position

try:
  import RPi
  import RPi.GPIO
except ModuleNotFoundError:  # pramga: no cover
  patch_module("fake_rpi.RPi")
  import fake_rpi.RPi as RPi  # pramga: no cover  pylint: disable=consider-using-from-import
