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
  @pytest.mark.parametrize(
      "platform_name", ["mocked_platform_arm32", "mocked_platform_arm64"]
  )
  def test__env__arm__no_substitute_given__patches_module(
      self,
      mocked_module_name: str,
      platform_name: str,
      request: pytest.FixtureRequest,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    mocked_platform = request.getfixturevalue(platform_name)
    monkeypatch.setattr(patch.os, "uname", mocked_platform)

    patch.patch_module(mocked_module_name)

    assert mocked_module_name in sys.modules
    assert isinstance(sys.modules[mocked_module_name], mock.Mock)

  @mock.patch.dict(
      patch.os.environ,
      {"PI_PORTAL_MOCK_GPIO": "True"},
      clear=True,
  )
  @pytest.mark.parametrize(
      "platform_name", ["mocked_platform_arm32", "mocked_platform_arm64"]
  )
  def test__env__arm__substitute_given__patches_module(
      self,
      mocked_module_name: str,
      mocked_substitute_name: str,
      platform_name: str,
      request: pytest.FixtureRequest,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    mocked_platform = request.getfixturevalue(platform_name)
    monkeypatch.setattr(patch.os, "uname", mocked_platform)

    patch.patch_module(mocked_module_name, mocked_substitute_name)

    assert mocked_module_name in sys.modules
    assert isinstance(sys.modules[mocked_module_name], mock.Mock)

  @mock.patch.dict(
      patch.os.environ,
      {"PI_PORTAL_MOCK_GPIO": "True"},
      clear=True,
  )
  def test__env__x86__no_substitute_given__patches_module(
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
  def test__env__x86__substitute_given__patches_module(
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
  @pytest.mark.parametrize(
      "platform_name", ["mocked_platform_arm32", "mocked_platform_arm64"]
  )
  def test__no_env__arm__no_substitute_given__loads_module(
      self,
      mocked_module_name: str,
      monkeypatch: pytest.MonkeyPatch,
      platform_name: str,
      request: pytest.FixtureRequest,
  ) -> None:
    mocked_platform = request.getfixturevalue(platform_name)
    monkeypatch.setattr(patch.os, "uname", mocked_platform)

    patch.patch_module(mocked_module_name)

    assert mocked_module_name not in sys.modules

  @mock.patch.dict(patch.os.environ, {}, clear=True)
  @pytest.mark.parametrize(
      "platform_name", ["mocked_platform_arm32", "mocked_platform_arm64"]
  )
  def test__no_env__arm__substitute_given__loads_module(
      self,
      mocked_module_name: str,
      mocked_substitute_name: str,
      monkeypatch: pytest.MonkeyPatch,
      platform_name: str,
      request: pytest.FixtureRequest,
  ) -> None:
    mocked_platform = request.getfixturevalue(platform_name)
    monkeypatch.setattr(patch.os, "uname", mocked_platform)

    patch.patch_module(mocked_module_name, mocked_substitute_name)

    assert mocked_module_name not in sys.modules

  @mock.patch.dict(patch.os.environ, {}, clear=True)
  def test__no_env__x86__no_substitute_given__patches_module(
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
  def test__no_env__x86__substitute_given__patches_substitute(
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
