"""Test fixtures for the CLI tests."""

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
  return CliRunner()
