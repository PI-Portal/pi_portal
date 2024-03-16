"""RemoteFileLogzIoAction class."""

from pi_portal.installation.actions.action_remote_files import (
    RemoteFile,
    RemoteFilesAction,
)


class RemoteFileLogzIoAction(RemoteFilesAction):
  """Download the required logz.io integration files."""

  remote_files = [
      RemoteFile(
          permissions="644",
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
          user="root",
          group="root",
      )
  ]
