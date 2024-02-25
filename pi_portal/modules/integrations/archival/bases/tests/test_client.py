"""Test the ArchivalClientBase class."""
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from ..client import ArchivalClientBase


@pytest.mark.usefixtures("test_state")
class TestArchivalClientBase:
  """Test the ArchivalClientBase class."""

  def test_initialization__attributes(
      self,
      concrete_archival_client_instance: ArchivalClientBase,
      mocked_partition_name: str,
  ) -> None:
    assert concrete_archival_client_instance.partition_name == (
        mocked_partition_name
    )

  def test_initialization__state(
      self,
      concrete_archival_client_instance: ArchivalClientBase,
      test_state: state.State,
  ) -> None:
    assert isinstance(test_state, state.State)
    assert concrete_archival_client_instance.current_state.user_config == (
        test_state.user_config
    )

  def test_upload__calls_underlying_implementation(
      self,
      concrete_archival_client_instance: ArchivalClientBase,
      mocked_archival_implementation: mock.Mock,
  ) -> None:
    mock_file_name = "mock_file_name"
    mock_archival_file_name = "mock_archival_file_name"

    concrete_archival_client_instance.upload(
        mock_file_name,
        mock_archival_file_name,
    )

    mocked_archival_implementation.upload.assert_called_once_with(
        mock_file_name,
        mock_archival_file_name,
    )
