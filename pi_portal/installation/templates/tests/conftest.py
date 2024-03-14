"""Test fixtures for the templates modules tests."""
# pylint: disable=redefined-outer-name

import pytest
from .. import config_file

CONFIG_FILE_MODULE = config_file.__name__


@pytest.fixture
def mocked_destination_file() -> str:
  return "/path/b/config_file.yml"


@pytest.fixture
def mocked_source_file() -> str:
  return "/path/a/config_file.yml"


@pytest.fixture
def config_file_template(
    mocked_destination_file: str,
    mocked_source_file: str,
) -> config_file.ConfileFileTemplate:
  return config_file.ConfileFileTemplate(
      permissions="644",
      destination=mocked_destination_file,
      source=mocked_source_file,
      user="test_user1",
  )
