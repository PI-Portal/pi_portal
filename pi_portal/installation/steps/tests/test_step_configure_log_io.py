"""Test the StepConfigureLogzIo class."""
import logging
from io import StringIO
from unittest import mock

from pi_portal.installation.templates import logzio_templates
from ..bases import remote_file_step
from ..step_configure_logz_io import StepConfigureLogzIo


class TestStepConfigureLogzIo:
  """Test the StepConfigureLogzIo class."""

  def test__initialize__attrs(
      self,
      step_configure_logz_io_instance: StepConfigureLogzIo,
  ) -> None:
    assert isinstance(step_configure_logz_io_instance.log, logging.Logger)
    assert step_configure_logz_io_instance.templates == logzio_templates

  def test__initialize__remote_files(
      self,
      step_configure_logz_io_instance: StepConfigureLogzIo,
  ) -> None:
    assert len(step_configure_logz_io_instance.remote_files) == 1
    logio_cert = step_configure_logz_io_instance.remote_files[0]
    assert isinstance(logio_cert, remote_file_step.RemoteFile)
    assert logio_cert.target == (
        "/etc/pki/tls/certs/COMODORSADomainValidationSecureServerCA.crt"
    )
    assert logio_cert.url == (
        "https://raw.githubusercontent.com/logzio/public-certificates/"
        "master/AAACertificateServices.crt"
    )
    assert logio_cert.permissions == "644"
    assert logio_cert.user == "root"

  def test__invoke__logging(
      self,
      step_configure_logz_io_instance: StepConfigureLogzIo,
      mocked_stream: StringIO,
  ) -> None:
    step_configure_logz_io_instance.invoke()

    assert mocked_stream.getvalue() == (
        "test - INFO - Configuring the logz.io integration ...\n"
        "test - INFO - Done configuring the logz.io integration.\n"
    )

  def test__invoke__download_call(
      self,
      step_configure_logz_io_instance: StepConfigureLogzIo,
      mocked_remote_file_download: mock.Mock,
  ) -> None:
    step_configure_logz_io_instance.invoke()

    mocked_remote_file_download.assert_called_once_with()

  def test__invoke__render_call(
      self,
      step_configure_logz_io_instance: StepConfigureLogzIo,
      mocked_template_render: mock.Mock,
  ) -> None:
    step_configure_logz_io_instance.invoke()

    mocked_template_render.assert_called_once_with()
