"""StepConfigureLogzIo class."""

from typing import List

from pi_portal.installation.templates import config_file, logzio_templates
from .bases import remote_file_step, render_templates_step


class StepConfigureLogzIo(
    remote_file_step.RemoteFileStepBase,
    render_templates_step.RenderTemplateStepBase,
):
  """Configure the logz.io integration."""

  remote_files = [
      remote_file_step.RemoteFile(
          sha256=(
              "a5ddabd1602ae1c66ce11ad078e734cc473dcb8e9f573037832d8536ae3de9"
              "0b"
          ),
          target=(
              "/etc/pki/tls/certs/COMODORSADomainValidationSecureServerCA.crt"
          ),
          url=(
              "https://raw.githubusercontent.com/logzio/public-certificates/"
              "master/AAACertificateServices.crt"
          ),
      )
  ]
  templates: List[config_file.ConfileFileTemplate] = logzio_templates

  def invoke(self) -> None:
    """Configure the logz.io integration."""

    self.log.info("Configuring the logz.io integration ...")
    self.render()
    self.download()
    self.log.info("Done configuring the logz.io integration.")
