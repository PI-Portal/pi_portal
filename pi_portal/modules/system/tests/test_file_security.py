"""Test the FileSecurity class."""

from unittest import mock

import pytest
from .. import file_security


class TestFileSecurity:
  """Test the FileSecurity class."""

  def test_intialize__attributes(
      self,
      file_security_instance: file_security.FileSecurity,
      mocked_file_path: str,
  ) -> None:
    assert file_security_instance.file_path == mocked_file_path
    assert file_security_instance.buffer_size == 65536

  def test_sha256__matches_expected_hash__no_exception(
      self,
      file_security_instance: file_security.FileSecurity,
      mocked_binary_data: bytes,
      mocked_hashlib_sha256: mock.Mock,
      mocked_open_read_binary: mock.Mock,
  ) -> None:
    mocked_hashlib_sha256.return_value.hexdigest.return_value = "hash_value"

    file_security_instance.sha256("hash_value")

    mocked_open_read_binary.assert_called_once_with(
        file_security_instance.file_path,
        "rb",
    )
    mocked_hashlib_sha256.return_value.update.assert_called_once_with(
        mocked_binary_data
    )

  def test_sha256__does_not_match_expected_hash__raises_exception(
      self,
      file_security_instance: file_security.FileSecurity,
      mocked_binary_data: bytes,
      mocked_hashlib_sha256: mock.Mock,
      mocked_open_read_binary: mock.Mock,
  ) -> None:
    mocked_hashlib_sha256.return_value.hexdigest.return_value = "hash_value"

    with pytest.raises(file_security.FileSecurityViolation) as exc:
      file_security_instance.sha256("wrong_hash_value")

    mocked_open_read_binary.assert_called_once_with(
        file_security_instance.file_path,
        "rb",
    )
    mocked_hashlib_sha256.return_value.update.assert_called_once_with(
        mocked_binary_data
    )
    assert str(exc.value) == file_security_instance.file_path
