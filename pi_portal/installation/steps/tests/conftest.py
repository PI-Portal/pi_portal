"""Fixtures for the steps modules tests."""
import logging
from io import StringIO
from typing import cast
from unittest import mock

import pytest
from pi_portal.installation.templates import config_file
from pi_portal.modules.configuration.logging import installer
from .. import (
    step_ensure_root,
    step_initialize_logging,
    step_install_config_file,
    step_kill_motion,
    step_kill_supervisor,
    step_render_templates,
    step_start_supervisor,
)
from ..bases import process_step, system_call_step

# pylint: disable=redefined-outer-name


@pytest.fixture
def mocked_config_file() -> str:
  return "/etc/motion/motion.conf"


@pytest.fixture
def mocked_copy() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_pid_file() -> str:
  return "/var/run/motion/motion.pid"


@pytest.fixture
def mocked_process_kill() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_system() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_template_render() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def installer_logger_stdout(mocked_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test")
  installer.InstallerLoggerConfiguration().configure(logger)
  cast(logging.StreamHandler, logger.handlers[0]).stream = mocked_stream
  return logger


@pytest.fixture
def step_ensure_root_instance(
    installer_logger_stdout: logging.Logger,
) -> step_ensure_root.StepEnsureRoot:
  return step_ensure_root.StepEnsureRoot(installer_logger_stdout)


@pytest.fixture
def step_initialize_logging_instance(
    installer_logger_stdout: logging.Logger,
    mocked_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_initialize_logging.StepInitializeLogging:
  monkeypatch.setattr(system_call_step.__name__ + ".os.system", mocked_system)
  return step_initialize_logging.StepInitializeLogging(installer_logger_stdout)


@pytest.fixture
def step_install_config_files_instance(
    installer_logger_stdout: logging.Logger,
    mocked_config_file: str,
    mocked_copy: mock.Mock,
    mocked_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_install_config_file.StepInstallConfigFile:
  monkeypatch.setattr(system_call_step.__name__ + ".os.system", mocked_system)
  monkeypatch.setattr(
      step_install_config_file.__name__ + ".shutil.copy", mocked_copy
  )
  return step_install_config_file.StepInstallConfigFile(
      installer_logger_stdout,
      mocked_config_file,
  )


@pytest.fixture
def step_kill_motion_instance(
    installer_logger_stdout: logging.Logger,
    mocked_pid_file: str,
    mocked_process_kill: mock.Mock,
    mocked_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_kill_motion.StepKillMotion:
  monkeypatch.setattr(
      process_step.__name__ + ".process.Process.kill", mocked_process_kill
  )
  monkeypatch.setattr(system_call_step.__name__ + ".os.system", mocked_system)
  return step_kill_motion.StepKillMotion(
      installer_logger_stdout,
      mocked_pid_file,
  )


@pytest.fixture
def step_kill_supervisor_instance(
    installer_logger_stdout: logging.Logger,
    mocked_pid_file: str,
    mocked_process_kill: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_kill_supervisor.StepKillSupervisor:
  monkeypatch.setattr(
      process_step.__name__ + ".process.Process.kill", mocked_process_kill
  )
  return step_kill_supervisor.StepKillSupervisor(
      installer_logger_stdout,
      mocked_pid_file,
  )


@pytest.fixture
def step_render_templates_instance(
    installer_logger_stdout: logging.Logger,
    mocked_system: mock.Mock,
    mocked_template_render: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_render_templates.StepRenderTemplates:
  monkeypatch.setattr(system_call_step.__name__ + ".os.system", mocked_system)
  monkeypatch.setattr(
      config_file.__name__ + ".ConfileFileTemplate.render",
      mocked_template_render
  )
  return step_render_templates.StepRenderTemplates(installer_logger_stdout)


@pytest.fixture
def step_start_supervisor_instance(
    installer_logger_stdout: logging.Logger,
    mocked_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_start_supervisor.StepStartSupervisor:
  monkeypatch.setattr(system_call_step.__name__ + ".os.system", mocked_system)
  return step_start_supervisor.StepStartSupervisor(installer_logger_stdout)
