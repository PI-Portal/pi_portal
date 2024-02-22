"""Test the tasks service bootstrapping."""
from unittest import mock

import pytest
from .. import create_service


@pytest.mark.usefixtures("setup_service_creation_mocks")
class TestCreateService:
  """Test the tasks service bootstrapping."""

  def test_create_service__imports_correct_module(
      self,
      mocked_import_module: mock.Mock,
  ) -> None:
    create_service()

    mocked_import_module.assert_called_once_with(
        "pi_portal.modules.tasks.service"
    )

  def test_create_service__returns_api_instance(
      self,
      mocked_import_module: mock.Mock,
  ) -> None:
    mocked_service_class = (
        mocked_import_module.return_value.TaskSchedulerService
    )

    result = create_service()

    assert result == mocked_service_class.return_value.server.api
