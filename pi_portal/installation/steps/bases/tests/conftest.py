"""Fixtures for the steps modules base class tests."""
# pylint: disable=redefined-outer-name,duplicate-code

import logging
from io import StringIO
from typing import TYPE_CHECKING, TextIO, cast
from unittest import mock

import pytest
from pi_portal.installation.templates import config_file
from pi_portal.modules.configuration.logging import installer
from .. import (
    remote_file_step,
    render_templates_step,
    service_step,
    system_call_step,
)

if TYPE_CHECKING:
  StreamHandlerType = logging.StreamHandler[TextIO]  # pragma: no cover
else:
  StreamHandlerType = logging.StreamHandler


@pytest.fixture
def mocked_file_security() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_http_client() -> mock.Mock:
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


class ConcreteServiceStep(service_step.ServiceStepBase):

  def invoke(self) -> None:
    raise NotImplementedError  # pragma: no cover


class ConcreteRemoteFileStep(remote_file_step.RemoteFileStepBase):

  remote_files = [
      remote_file_step.RemoteFile(
          sha256="expected_sha256_1",
          target="/path/target1.txt",
          url="https://remote.com/source1.txt",
      ),
      remote_file_step.RemoteFile(
          sha256="expected_sha256_2",
          target="/path/target2.sh",
          url="https://remote.com/source2.sh",
          permissions="755",
          user="test_user",
      )
  ]

  def invoke(self) -> None:
    raise NotImplementedError  # pragma: no cover


class ConcreteRenderTemplateStep(
    render_templates_step.RenderTemplateStepBase,
):

  templates = [
      config_file.ConfileFileTemplate(
          source="templates/file1",
          destination="/etc/file1",
      ),
      config_file.ConfileFileTemplate(
          source="templates/file2",
          destination="/etc/file2",
          permissions="755",
          user="test_user",
      )
  ]

  def invoke(self) -> None:
    raise NotImplementedError  # pragma: no cover


@pytest.fixture
def installer_logger_stdout(mocked_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test")
  installer.InstallerLoggerConfiguration().configure(logger)
  installer_logger_handler = logger.handlers[0]
  cast(StreamHandlerType, installer_logger_handler).stream = mocked_stream
  return logger


@pytest.fixture
def service_definition_instance() -> service_step.ServiceDefinition:
  return service_step.ServiceDefinition(
      service_name="mock_service",
      system_v_service_name="mock_system_v_service",
      systemd_unit_name="mock_service_unit",
  )


@pytest.fixture()
def concrete_remote_file_step_instance(
    installer_logger_stdout: logging.Logger,
    mocked_file_security: mock.Mock,
    mocked_http_client: mock.Mock,
    mocked_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> remote_file_step.RemoteFileStepBase:
  monkeypatch.setattr(
      remote_file_step.__name__ + ".file_security.FileSecurity",
      mocked_file_security,
  )
  monkeypatch.setattr(
      remote_file_step.__name__ + ".http.HttpClient",
      mocked_http_client,
  )
  monkeypatch.setattr(
      system_call_step.__name__ + ".os.system",
      mocked_system,
  )
  return ConcreteRemoteFileStep(installer_logger_stdout)


@pytest.fixture
def concrete_render_templates_step_instance(
    installer_logger_stdout: logging.Logger,
    mocked_system: mock.Mock,
    mocked_template_render: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> render_templates_step.RenderTemplateStepBase:
  monkeypatch.setattr(system_call_step.__name__ + ".os.system", mocked_system)
  monkeypatch.setattr(
      config_file.__name__ + ".ConfileFileTemplate.render",
      mocked_template_render
  )
  return ConcreteRenderTemplateStep(installer_logger_stdout)


@pytest.fixture
def concrete_service_step_instance(
    installer_logger_stdout: logging.Logger,
    mocked_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
    service_definition_instance: service_step.ServiceDefinition,
) -> service_step.ServiceStepBase:
  monkeypatch.setattr(
      system_call_step.__name__ + ".os.system",
      mocked_system,
  )
  instance = ConcreteServiceStep(installer_logger_stdout)
  instance.service = service_definition_instance
  return instance
