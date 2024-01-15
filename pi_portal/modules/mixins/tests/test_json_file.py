"""Test the JSONFile mixin classes."""

import json
from io import StringIO

from .. import read_json_file


class TestJSONFileReader:
  """Test the JSONFileReader mixin class."""

  def test__initialize__attributes(
      self,
      json_file_reader_instance: read_json_file.JSONFileReader,
  ) -> None:
    assert json_file_reader_instance.encoding == "utf-8"

  def test__load_json_file__return_value(
      self,
      json_file_reader_instance: read_json_file.JSONFileReader,
      mocked_file_handle_string: StringIO,
  ) -> None:
    mock_path = "/mock/path"
    mock_object = {"mock": "object"}
    mocked_file_handle_string.write(json.dumps(mock_object))
    mocked_file_handle_string.seek(0)

    result = json_file_reader_instance.load_json_file(mock_path)

    assert result == mock_object
