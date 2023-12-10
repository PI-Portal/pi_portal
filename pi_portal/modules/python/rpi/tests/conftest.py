"""Fixtures for the python modules tests."""

import sys
from collections import namedtuple
from unittest import mock

import pytest

UnameTuple = namedtuple("Uname", "sysname nodename release version machine")


@pytest.fixture
def mocked_module_name() -> str:
  module_name = "test_module"
  sys.modules.pop(module_name, None)
  return module_name


@pytest.fixture
def mocked_platform_arm() -> mock.Mock:
  return mock.Mock(
      return_value=UnameTuple(
          "linux", "unknown", "6.4.16-linuxkit", "unknown version", "armv7l"
      )
  )


@pytest.fixture
def mocked_platform_x86() -> mock.Mock:
  return mock.Mock(
      return_value=UnameTuple(
          "linux", "unknown", "6.4.16-linuxkit", "unknown version", "x86_64"
      )
  )


@pytest.fixture
def mocked_substitute_name() -> str:
  module_name = "fake_rpi"
  sys.modules.pop(module_name, None)
  return module_name
