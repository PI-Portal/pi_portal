"""Test fixtures for the user cli commands tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from unittest import mock

import pytest
from .. import installer, version


@pytest.fixture
def mocked_click() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_name() -> str:
  return "/mock/path/mock.file"


@pytest.fixture
def mocked_installer() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def installer_command_instance(
    mocked_click: mock.Mock,
    mocked_file_name: str,
    mocked_installer: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> installer.InstallerCommand:
  monkeypatch.setattr(
      installer.__name__ + ".click",
      mocked_click,
  )
  monkeypatch.setattr(
      installer.__name__ + ".pi_portal_installer.Installer",
      mocked_installer,
  )
  return installer.InstallerCommand(mocked_file_name, False)


@pytest.fixture
def version_command_instance(
    mocked_click: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> version.VersionCommand:
  monkeypatch.setattr(
      version.__name__ + ".click",
      mocked_click,
  )
  return version.VersionCommand()
