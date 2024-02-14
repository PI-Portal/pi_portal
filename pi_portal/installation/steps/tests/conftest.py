"""Fixtures for the steps modules tests."""
# pylint: disable=duplicate-code

import logging
from io import StringIO
from typing import TYPE_CHECKING, TextIO, cast
from unittest import mock

import pytest
from pi_portal.modules.configuration.logging import installer
from .. import (
    step_configure_logz_io,
    step_configure_motion,
    step_ensure_root,
    step_initialize_data_paths,
    step_initialize_etc,
    step_initialize_logging,
    step_install_config_file,
    step_kill_motion,
    step_kill_supervisor,
    step_render_configuration,
    step_start_supervisor,
)
from ..bases import (
    remote_file_step,
    render_templates_step,
    service_step,
    system_call_step,
)

if TYPE_CHECKING:
  StreamHandlerType = logging.StreamHandler[TextIO]  # pragma: no cover
else:
  StreamHandlerType = logging.StreamHandler

# pylint: disable=redefined-outer-name


@pytest.fixture
def mocked_config_file() -> str:
  return "/etc/motion/motion.conf"


@pytest.fixture
def mocked_copy() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_system() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_remote_file_download() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_service_step_base_disable() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_service_step_base_enable() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_service_step_base_start() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_service_step_base_stop() -> mock.Mock:
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
  installer_logger_handler = logger.handlers[0]
  cast(StreamHandlerType, installer_logger_handler).stream = mocked_stream
  return logger


@pytest.fixture
def step_configure_logz_io_instance(
    installer_logger_stdout: logging.Logger,
    mocked_remote_file_download: mock.Mock,
    mocked_template_render: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_configure_logz_io.StepConfigureLogzIo:
  monkeypatch.setattr(
      remote_file_step.__name__ + ".RemoteFileStepBase.download",
      mocked_remote_file_download
  )
  monkeypatch.setattr(
      render_templates_step.__name__ + ".RenderTemplateStepBase.render",
      mocked_template_render
  )
  return step_configure_logz_io.StepConfigureLogzIo(installer_logger_stdout)


@pytest.fixture
def step_configure_motion_instance(
    installer_logger_stdout: logging.Logger,
    mocked_template_render: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_configure_motion.StepConfigureMotion:
  monkeypatch.setattr(
      render_templates_step.__name__ + ".RenderTemplateStepBase.render",
      mocked_template_render,
  )
  instance = step_configure_motion.StepConfigureMotion(installer_logger_stdout)
  return instance


@pytest.fixture
def step_ensure_root_instance(
    installer_logger_stdout: logging.Logger,
) -> step_ensure_root.StepEnsureRoot:
  return step_ensure_root.StepEnsureRoot(installer_logger_stdout)


@pytest.fixture
def step_initialize_data_paths_instance(
    installer_logger_stdout: logging.Logger,
    mocked_file_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_initialize_data_paths.StepInitializeDataPaths:
  monkeypatch.setattr(
      step_initialize_data_paths.__name__ + ".FileSystem", mocked_file_system
  )
  return step_initialize_data_paths.StepInitializeDataPaths(
      installer_logger_stdout
  )


@pytest.fixture
def step_initialize_etc_instance(
    installer_logger_stdout: logging.Logger,
    mocked_file_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_initialize_etc.StepInitializeEtc:
  monkeypatch.setattr(
      step_initialize_etc.__name__ + ".FileSystem", mocked_file_system
  )
  return step_initialize_etc.StepInitializeEtc(installer_logger_stdout)


@pytest.fixture
def step_initialize_logging_instance(
    installer_logger_stdout: logging.Logger,
    mocked_file_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_initialize_logging.StepInitializeLogging:
  monkeypatch.setattr(
      step_initialize_logging.__name__ + ".FileSystem", mocked_file_system
  )
  return step_initialize_logging.StepInitializeLogging(installer_logger_stdout)


@pytest.fixture
def step_install_config_files_instance(
    installer_logger_stdout: logging.Logger,
    mocked_config_file: str,
    mocked_copy: mock.Mock,
    mocked_file_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_install_config_file.StepInstallConfigFile:
  monkeypatch.setattr(
      step_install_config_file.__name__ + ".FileSystem", mocked_file_system
  )
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
    mocked_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
    mocked_service_step_base_disable: mock.Mock,
    mocked_service_step_base_stop: mock.Mock,
) -> step_kill_motion.StepKillMotion:
  monkeypatch.setattr(
      service_step.__name__ + ".ServiceStepBase.disable",
      mocked_service_step_base_disable
  )
  monkeypatch.setattr(
      service_step.__name__ + ".ServiceStepBase.stop",
      mocked_service_step_base_stop
  )
  monkeypatch.setattr(system_call_step.__name__ + ".os.system", mocked_system)
  return step_kill_motion.StepKillMotion(installer_logger_stdout,)


@pytest.fixture
def step_kill_supervisor_instance(
    installer_logger_stdout: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
    mocked_service_step_base_stop: mock.Mock,
) -> step_kill_supervisor.StepKillSupervisor:
  monkeypatch.setattr(
      service_step.__name__ + ".ServiceStepBase.stop",
      mocked_service_step_base_stop
  )
  return step_kill_supervisor.StepKillSupervisor(installer_logger_stdout,)


@pytest.fixture
def step_render_configuration_instance(
    installer_logger_stdout: logging.Logger,
    mocked_template_render: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_render_configuration.StepRenderConfiguration:
  monkeypatch.setattr(
      render_templates_step.__name__ + ".RenderTemplateStepBase.render",
      mocked_template_render,
  )
  return step_render_configuration.StepRenderConfiguration(
      installer_logger_stdout,
  )


@pytest.fixture
def step_start_supervisor_instance(
    installer_logger_stdout: logging.Logger,
    mocked_service_step_base_enable: mock.Mock,
    mocked_service_step_base_start: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> step_start_supervisor.StepStartSupervisor:
  monkeypatch.setattr(
      service_step.__name__ + ".ServiceStepBase.enable",
      mocked_service_step_base_enable,
  )
  monkeypatch.setattr(
      service_step.__name__ + ".ServiceStepBase.start",
      mocked_service_step_base_start,
  )
  return step_start_supervisor.StepStartSupervisor(installer_logger_stdout)
