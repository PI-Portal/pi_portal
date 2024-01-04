"""Validate entities on the local file system."""

from hashlib import sha256


class FileSecurityViolation(Exception):
  """Raised when a local file fails a security check."""


class FileSecurity:
  """Methods to validate the authenticity of local file system content.

  :param file_path: The path to the local file.
  """

  file_path: str
  buffer_size = 65536

  def __init__(self, file_path: str) -> None:
    self.file_path = file_path

  def sha256(self, expected_hash: str) -> None:
    """Validate the sha256 digest of this file against an expected value.

    :param expected_hash: The expected sha256 digest.
    :raises: :class:`FileSecurityViolation`
    """
    calculated_hash = sha256()
    with open(self.file_path, "rb") as file_handle:
      data = file_handle.read(self.buffer_size)
      while data:
        calculated_hash.update(data)
        data = file_handle.read(self.buffer_size)
    if calculated_hash.hexdigest() != expected_hash:
      raise FileSecurityViolation(self.file_path)
