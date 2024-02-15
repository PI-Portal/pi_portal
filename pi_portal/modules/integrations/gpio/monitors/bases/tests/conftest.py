"""Test fixtures for the GPIO monitor base module tests."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO
from typing import Callable, List, Type
from unittest import mock

import pytest
from pi_portal.modules.integrations.gpio.components.bases.input_base import (
    GPIOInputBase,
)
from .. import monitor_base
from ..monitor_base import GPIOMonitorBase

TypeGenericGpioInput = GPIOInputBase[mock.Mock]
TypeGenericGpioMonitor = GPIOMonitorBase[TypeGenericGpioInput]


class Interrupt(Exception):
  """Raised during testing to interrupt polling loops."""


@pytest.fixture
def mocked_configure_logger() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_logger(mocked_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test")
  handler = logging.StreamHandler(stream=mocked_stream)
  handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  return logger


@pytest.fixture
def concrete_gpio_monitor_class(
    mocked_configure_logger: mock.Mock,
    mocked_sleep: mock.Mock,
    setup_monitor_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> Type[TypeGenericGpioMonitor]:
  setup_monitor_mocks()
  monkeypatch.setattr(
      monitor_base.__name__ + ".GPIOMonitorBase.configure_logger",
      mocked_configure_logger,
  )
  monkeypatch.setattr(
      monitor_base.__name__ + ".time.sleep",
      mocked_sleep,
  )

  class ConcreteGPIOMonitor(GPIOMonitorBase[TypeGenericGpioInput]):

    logger_name = "test_logger"
    log_file_path = "/var/log/non_existent.log"
    gpio_log_changes_only = True

    def hook_log_state(self, gpio_pin: TypeGenericGpioInput) -> None:
      self.log.info("%s -> %s", gpio_pin.pin_name, gpio_pin.current_state)

  return ConcreteGPIOMonitor


@pytest.fixture
def concrete_gpio_monitor_instance(
    concrete_gpio_monitor_class: Type[TypeGenericGpioMonitor],
    mocked_gpio_pins: List[mock.Mock],
    mocked_logger: logging.Logger,
) -> TypeGenericGpioMonitor:
  instance = concrete_gpio_monitor_class(mocked_gpio_pins)
  setattr(
      instance,
      "log",
      mocked_logger,
  )
  return instance
