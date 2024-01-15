"""Test the LogFileReader mixin class."""

import json
from io import BytesIO
from typing import Any, Dict, List
from unittest import mock

import pytest
from .. import read_log_file


class TestLogFileReader:
  """Test the LogFileReader mixin class."""

  def build_valid_json_log_data(
      self,
      mocked_file_handle_binary: BytesIO,
  ) -> List[str]:
    data = []
    for i in range(0, 10):
      json_data = json.dumps({str(i): "test data"})
      data.append(json_data)
    self.populate_file_handle(
        mocked_file_handle_binary,
        data,
    )
    return data

  def build_invalid_json_log_data(
      self,
      mocked_file_handle_binary: BytesIO,
  ) -> List[str]:
    data = ["Not Valid JSON"]
    for i in range(0, 4):
      json_data = json.dumps({str(i): "test data"})
      data.append(json_data)
    self.populate_file_handle(
        mocked_file_handle_binary,
        data,
    )
    return data

  def populate_file_handle(
      self,
      mocked_file_handle_binary: BytesIO,
      log_content: List[str],
  ) -> None:
    for line in log_content:
      mocked_file_handle_binary.write(
          line.encode(read_log_file.LogFileReader.log_file_encoding,) +
          read_log_file.LogFileReader.new_line_byte
      )

  def decode_json_log(self, data: List[str]) -> List[Dict[Any, Any]]:
    decoded_data = []
    for row in data:
      decoded_data.append(json.loads(row))
    return decoded_data

  def test__initialize__attributes(
      self,
      log_file_reader_instance: read_log_file.LogFileReader,
  ) -> None:
    assert log_file_reader_instance.log_file_encoding == "utf-8"
    assert log_file_reader_instance.new_line_byte == b'\n'

  def test__tail__1_line__seek_error(
      self, log_file_reader_instance: read_log_file.LogFileReader,
      mocked_file_handle_binary: BytesIO, monkeypatch: pytest.MonkeyPatch
  ) -> None:
    monkeypatch.setattr(
        mocked_file_handle_binary, "seek",
        mock.Mock(side_effect=[OSError, None])
    )

    log_data = log_file_reader_instance.tail(1)

    assert log_data == []

  def test__tail__1_line__valid_json(
      self,
      log_file_reader_instance: read_log_file.LogFileReader,
      mocked_file_handle_binary: BytesIO,
  ) -> None:
    mock_data = self.build_valid_json_log_data(mocked_file_handle_binary,)

    log_data = log_file_reader_instance.tail(1)

    assert log_data == self.decode_json_log(mock_data[9:])

  def test__tail__4_lines__valid_json(
      self,
      log_file_reader_instance: read_log_file.LogFileReader,
      mocked_file_handle_binary: BytesIO,
  ) -> None:
    mock_data = self.build_valid_json_log_data(mocked_file_handle_binary,)

    log_data = log_file_reader_instance.tail(4)

    assert log_data == self.decode_json_log(mock_data[6:])

  def test__tail__too_many_lines__valid_json(
      self,
      log_file_reader_instance: read_log_file.LogFileReader,
      mocked_file_handle_binary: BytesIO,
  ) -> None:
    mock_data = self.build_valid_json_log_data(mocked_file_handle_binary,)

    log_data = log_file_reader_instance.tail(20)

    assert log_data == self.decode_json_log(mock_data)

  def test__tail__1_line__invalid_json(
      self,
      log_file_reader_instance: read_log_file.LogFileReader,
      mocked_file_handle_binary: BytesIO,
  ) -> None:
    mock_data = self.build_invalid_json_log_data(mocked_file_handle_binary,)

    log_data = log_file_reader_instance.tail(5)

    assert log_data == self.decode_json_log(mock_data[1:])
