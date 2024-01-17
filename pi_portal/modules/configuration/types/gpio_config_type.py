"""GPIO configuration types."""

from typing import List

from typing_extensions import TypedDict


class TypeUserConfigSwitches(TypedDict):
  """Typed representation of GPIO connected switches."""

  CONTACT_SWITCHES: List["TypeUserConfigGPIO"]


class TypeUserConfigTemperatureSensors(TypedDict):
  """Typed representation of GPIO connected temperature sensors."""

  DHT11: List["TypeUserConfigGPIO"]


class TypeUserConfigGPIO(TypedDict):
  """Typed representation of a GPIO connected device."""

  NAME: str
  GPIO: int
