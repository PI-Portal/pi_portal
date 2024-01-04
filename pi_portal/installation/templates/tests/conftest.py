"""Test fixtures for the templates modules tests."""
# pylint: disable=redefined-outer-name

import pytest
from pi_portal.modules.configuration.tests.fixtures import mock_state
from .. import config_file

CONFIG_FILE_MODULE = config_file.__name__


@pytest.fixture
def mocked_source_file() -> str:
  return "/path/a/config_file.yml"


@pytest.fixture
def mocked_destination_file() -> str:
  return "/path/b/config_file.yml"


@pytest.fixture
def config_file_template(
    mocked_source_file: str,
    mocked_destination_file: str,
) -> config_file.ConfileFileTemplate:
  with mock_state.mock_state_creator():
    return config_file.ConfileFileTemplate(
        source=mocked_source_file,
        destination=mocked_destination_file,
    )
