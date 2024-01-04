"""Test fixtures for the installation modules tests."""
# pylint: disable=redefined-outer-name

from io import StringIO
from typing import List
from unittest import mock

import pytest
from .. import installer, steps
from ..steps.bases import base_step

BASE_STEP_MODULE = base_step.__name__
INSTALLER_MODULE = installer.__name__

step_sequence = [
    steps.StepEnsureRoot,
    steps.StepKillMotion,
    steps.StepKillSupervisor,
    steps.StepInitializeDataPaths,
    steps.StepInitializeEtc,
    steps.StepInitializeLogging,
    steps.StepRenderConfiguration,
    steps.StepInstallConfigFile,
    steps.StepConfigureLogzIo,
    steps.StepStartSupervisor,
]


@pytest.fixture
def mocked_config_file_path() -> str:
  return "/home/pi/config.json"


@pytest.fixture
def mocked_steps() -> List[mock.Mock]:
  return [
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
      mock.Mock(),
  ]


@pytest.fixture
def mocked_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def installer_instance(
    mocked_steps: List[mock.Mock],
    mocked_stream: StringIO,
    monkeypatch: pytest.MonkeyPatch,
    mocked_config_file_path: str,
) -> installer.Installer:
  mock_index = 0
  for step in step_sequence:
    monkeypatch.setattr(
        INSTALLER_MODULE + "." + step.__name__, mocked_steps[mock_index]
    )
    mock_index += 1
  instance = installer.Installer(mocked_config_file_path)
  monkeypatch.setattr(instance.log.handlers[0], "stream", mocked_stream)
  return instance
