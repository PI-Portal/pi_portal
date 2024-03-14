"""Test the RemoteFileLogzIoAction class."""

from ...utility.generate_action_remote_files_test import (
    GenericRemoteFilesActionTest,
)
from .. import action_remote_files


class TestRemoteFileLogzIoAction(GenericRemoteFilesActionTest):
  """Test the RemoteFileLogzIoAction class."""

  action_class = action_remote_files.RemoteFileLogzIoAction

  def test_initialize__attributes__remote_files(self) -> None:
    assert len(self.action_class.remote_files) == 1

  def test_initialize__attributes__file_beat_cert(self) -> None:
    file_beat_cert = self.action_class.remote_files[0]
    assert file_beat_cert.permissions == "644"
    assert file_beat_cert.sha256 == (
        "a5ddabd1602ae1c66ce11ad078e734cc473dcb8e9f573037832d8536ae3de9"
        "0b"
    )
    assert file_beat_cert.target == (
        "/etc/pki/tls/certs/COMODORSADomainValidationSecureServerCA.crt"
    )
    assert file_beat_cert.url == (
        "https://raw.githubusercontent.com/logzio/public-certificates/"
        "master/AAACertificateServices.crt"
    )
    assert file_beat_cert.user == "root"
