"""Test the ReadLogFile mixin class."""

import json
from contextlib import closing
from io import BytesIO
from typing import Any, Dict, List, cast
from unittest import mock

from .. import read_log_file

LOG_FILE_MODULE = read_log_file.__name__


class TestReadLogFile:
  """Test the WriteLogFile mixin class."""

  def create_file_handle(self, source: List[str]) -> mock.MagicMock:
    """Test double for a Pi Portal log file."""
    mock_read_data = "\n".join(source)
    return mock.MagicMock(
        return_value=closing(BytesIO(mock_read_data.encode("utf-8")))
    )

  def create_valid_json_log_data(self) -> List[str]:
    data = []
    for i in range(0, 10):
      data.append(json.dumps({str(i): "test data"}))
    return data

  def create_invalid_json_log_data(self) -> List[str]:
    data = ["Not Valid JSON"]
    for i in range(0, 4):
      data.append(json.dumps({str(i): "test data"}))
    return data

  def parse_json_log_data(self, data: List[str]) -> List[Dict[Any, Any]]:
    decoded_data = []
    for row in data:
      decoded_data.append(json.loads(row))
    return decoded_data

  def test_tail__1_line__seek_error(
      self,
      instance: read_log_file.LogFileReader,
  ) -> None:
    with mock.patch("io.BytesIO") as log_file_content:
      log_file_content.seek.side_effect = [OSError, None]
    with mock.patch(
        LOG_FILE_MODULE + '.open',
        mock.Mock(return_value=closing(cast(BytesIO, log_file_content)))
    ):

      log_data = instance.tail(1)

    assert log_data == []

  def test_tail__1_line__valid_json(
      self,
      instance: read_log_file.LogFileReader,
  ) -> None:
    with mock.patch(
        LOG_FILE_MODULE + '.open',
        self.create_file_handle(self.create_valid_json_log_data())
    ):

      log_data = instance.tail(1)

    assert log_data == self.parse_json_log_data(
        self.create_valid_json_log_data()[9:],
    )

  def test_tail__4_lines__valid_json(
      self,
      instance: read_log_file.LogFileReader,
  ) -> None:
    with mock.patch(
        LOG_FILE_MODULE + '.open',
        self.create_file_handle(self.create_valid_json_log_data())
    ):

      log_data = instance.tail(4)

    assert log_data == self.parse_json_log_data(
        self.create_valid_json_log_data()[6:],
    )

  def test_tail__too_many_lines__valid_json(
      self,
      instance: read_log_file.LogFileReader,
  ) -> None:
    with mock.patch(
        LOG_FILE_MODULE + '.open',
        self.create_file_handle(self.create_valid_json_log_data())
    ):

      log_data = instance.tail(20)

    assert log_data == self.parse_json_log_data(
        self.create_valid_json_log_data(),
    )

  def test_tail__1_line__invalid_json(
      self,
      instance: read_log_file.LogFileReader,
  ) -> None:
    with mock.patch(
        LOG_FILE_MODULE + '.open',
        self.create_file_handle(self.create_invalid_json_log_data())
    ):

      log_data = instance.tail(5)

    assert log_data == self.parse_json_log_data(
        self.create_invalid_json_log_data()[1:],
    )
