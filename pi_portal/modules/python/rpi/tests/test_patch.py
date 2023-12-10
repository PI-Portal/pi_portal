"""Test the patch_rpi_gpio function."""

import sys
from unittest import mock

import pytest
from .. import patch

PATCH_MODULE = patch.__name__


class TestPatchModule:
  """Test the patch_module function."""

  @mock.patch.dict(
      patch.os.environ,
      {"PI_PORTAL_MOCK_GPIO": "True"},
      clear=True,
  )
  def test__docker_testing__arm_platform__no_substitute(
      self,
      mocked_module_name: str,
      mocked_platform_arm: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_arm)

    patch.patch_module(mocked_module_name)

    assert mocked_module_name in sys.modules
    assert isinstance(sys.modules[mocked_module_name], mock.Mock)

  @mock.patch.dict(
      patch.os.environ,
      {"PI_PORTAL_MOCK_GPIO": "True"},
      clear=True,
  )
  def test__docker_testing__arm_platform__substitute(
      self,
      mocked_module_name: str,
      mocked_substitute_name: str,
      mocked_platform_arm: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_arm)

    patch.patch_module(mocked_module_name, mocked_substitute_name)

    assert mocked_module_name in sys.modules
    assert isinstance(sys.modules[mocked_module_name], mock.Mock)

  @mock.patch.dict(
      patch.os.environ,
      {"PI_PORTAL_MOCK_GPIO": "True"},
      clear=True,
  )
  def test__docker_testing__x86_platform__no_substitute(
      self,
      mocked_module_name: str,
      mocked_platform_x86: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_x86)

    patch.patch_module(mocked_module_name)

    assert mocked_module_name in sys.modules
    assert isinstance(sys.modules[mocked_module_name], mock.Mock)

  @mock.patch.dict(
      patch.os.environ,
      {"PI_PORTAL_MOCK_GPIO": "True"},
      clear=True,
  )
  def test__docker_testing__x86_platform__substitute(
      self,
      mocked_module_name: str,
      mocked_substitute_name: str,
      mocked_platform_x86: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_x86)

    patch.patch_module(mocked_module_name, mocked_substitute_name)

    assert mocked_module_name in sys.modules
    assert isinstance(sys.modules[mocked_module_name], mock.Mock)

  @mock.patch.dict(patch.os.environ, {}, clear=True)
  def test__not_docker_testing__arm_platform__no_substitute(
      self,
      mocked_module_name: str,
      mocked_platform_arm: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_arm)

    patch.patch_module(mocked_module_name)

    assert mocked_module_name not in sys.modules

  @mock.patch.dict(patch.os.environ, {}, clear=True)
  def test__not_docker_testing__arm_platform__substitute(
      self,
      mocked_module_name: str,
      mocked_substitute_name: str,
      mocked_platform_arm: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_arm)

    patch.patch_module(mocked_module_name, mocked_substitute_name)

    assert mocked_module_name not in sys.modules

  @mock.patch.dict(patch.os.environ, {}, clear=True)
  def test__not_docker_testing__x86__no_substitute(
      self,
      mocked_module_name: str,
      mocked_platform_x86: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_x86)

    patch.patch_module(mocked_module_name)

    assert mocked_module_name in sys.modules
    assert isinstance(sys.modules[mocked_module_name], mock.Mock)

  @mock.patch.dict(patch.os.environ, {}, clear=True)
  def test__not_docker_testing__x86__substitute(
      self,
      mocked_module_name: str,
      mocked_substitute_name: str,
      mocked_platform_x86: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    monkeypatch.setattr(patch.os, "uname", mocked_platform_x86)

    patch.patch_module(mocked_module_name, mocked_substitute_name)

    assert mocked_module_name in sys.modules
    assert not isinstance(sys.modules[mocked_module_name], mock.Mock)
    assert sys.modules[mocked_module_name] == sys.modules[mocked_substitute_name
                                                         ]
