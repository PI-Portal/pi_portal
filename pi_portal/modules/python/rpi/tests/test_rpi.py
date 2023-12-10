"""Tests for the patched rpi module."""

import importlib
import os
import sys
from unittest import mock

import pytest
from adafruit_platformdetect.constants import boards
from .. import patch


@mock.patch("adafruit_blinka.agnostic.board_id", boards.GENERIC_LINUX_PC)
class TestPatchedRpiModule:
  """Tests for the patched rpi module."""

  def setup_method(self) -> None:
    sys.modules.pop('pi_portal.modules.python.rpi', None)
    sys.modules.pop('adafruit_dht', None)
    sys.modules.pop('board', None)
    sys.modules.pop('RPi', None)

  @mock.patch.dict(os.environ, {"PI_PORTAL_MOCK_GPIO": "1"}, clear=True)
  def test__arm_platform__docker_testing(
      self,
      mocked_platform_arm: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_arm)

    rpi = importlib.import_module("pi_portal.modules.python.rpi")

    assert isinstance(rpi.adafruit_dht, mock.Mock)
    assert isinstance(rpi.board, mock.Mock)
    assert isinstance(rpi.RPi, mock.Mock)

  @mock.patch.dict(os.environ, {}, clear=True)
  def test__arm_platform__not_docker_testing(
      self,
      mocked_platform_arm: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_arm)

    rpi = importlib.import_module("pi_portal.modules.python.rpi")

    assert not isinstance(rpi.adafruit_dht, mock.Mock)
    assert not isinstance(rpi.board, mock.Mock)
    assert not isinstance(rpi.RPi, mock.Mock)

  @mock.patch.dict(os.environ, {"PI_PORTAL_MOCK_GPIO": "1"}, clear=True)
  def test__x86_platform__docker_testing(
      self,
      mocked_platform_x86: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(os, "uname", mocked_platform_x86)

    rpi = importlib.import_module("pi_portal.modules.python.rpi")

    assert isinstance(rpi.adafruit_dht, mock.Mock)
    assert isinstance(rpi.board, mock.Mock)
    assert isinstance(rpi.RPi, mock.Mock)

  @mock.patch.dict(os.environ, {}, clear=True)
  def test__x86_platform__not_docker_testing(
      self,
      mocked_platform_x86: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(os, "uname", mocked_platform_x86)

    rpi = importlib.import_module("pi_portal.modules.python.rpi")
    fake_rpi = importlib.import_module("fake_rpi.RPi")

    assert isinstance(rpi.adafruit_dht, mock.Mock)
    assert isinstance(rpi.board, mock.Mock)
    assert rpi.RPi == fake_rpi
