"""Standard logging mixin class."""

import json
import os
from typing import Any, Dict, List


class LogFileReader:
  """Adds logging features to an existing class."""

  log_file_path: str
  log_file_encoding: str = "utf-8"
  new_line_byte: bytes = b'\n'

  def tail(self, requested_lines: int) -> List[Dict[Any, Any]]:
    """Read the specified number of lines from the end of a log file.

    Lines that are not JSON formatted are dropped silently.

    :param requested_lines: The number of lines to read.
    :returns: An array containing the lines read from the log file.
    """

    raw_bytes_tail = self._read_bytes_tail(requested_lines)
    log_tail = self._convert_bytes_tail_to_string_tail(raw_bytes_tail)
    return log_tail

  def _read_bytes_tail(self, requested_lines: int) -> bytes:
    read_lines = 0
    with open(self.log_file_path, "rb") as file_handle:
      try:
        file_handle.seek(-2, os.SEEK_END)
        while read_lines < requested_lines and file_handle.tell() > 0:
          if file_handle.read(1) == self.new_line_byte:
            read_lines += 1
          file_handle.seek(-2, os.SEEK_CUR)
      except OSError:
        file_handle.seek(0)
      finally:
        raw_tail_bytes = file_handle.read()
    return raw_tail_bytes

  def _convert_bytes_tail_to_string_tail(
      self, raw_tail_bytes: bytes
  ) -> List[Dict[Any, Any]]:
    bytes_log_tail = raw_tail_bytes.split(self.new_line_byte)
    string_log_tail = []
    for bytes_line in bytes_log_tail:
      if len(bytes_line) > 1:
        try:
          string_log_tail.append(
              json.loads(bytes_line.decode(self.log_file_encoding),),
          )
        except json.JSONDecodeError:
          pass

    return string_log_tail
