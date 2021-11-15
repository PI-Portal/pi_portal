"""User configuration loader."""

import json
import os


def load():
  """Load the end user's configuration file."""

  if "SPHINX" in os.environ:
    return {}

  with open("config.json", "r", encoding="utf-8") as file_handle:
    user_config = json.load(file_handle)

  return user_config
