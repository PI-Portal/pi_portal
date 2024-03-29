"""JSONFileReader mixin class."""

import json
from pathlib import Path
from typing import Any, Union


class JSONFileReader:
  """JSONFileReader mixin class."""

  encoding = "utf-8"

  def load_json_file(self, json_file_location: Union[Path, str]) -> Any:
    """Load a JSON file from the filesystem and return it as a Python object.

    :param json_file_location: The path to the source file.
    :returns: The loaded JSON object.
    """

    with open(json_file_location, encoding=self.encoding) as f_handle:
      json_file_content = json.load(f_handle)
    return json_file_content
