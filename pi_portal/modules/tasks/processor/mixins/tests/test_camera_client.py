"""Test the CameraClientMixin class."""
import logging

import pytest
from pi_portal.modules.integrations.camera.service_client import CameraClient
from pi_portal.modules.tasks.processor.mixins.camera_client import (
    CameraClientMixin,
)


@pytest.mark.usefixtures('test_state')
class TestCameraClientMixin:
  """Test the CameraClientMixin class."""

  def test_initialize__slack_client(
      self,
      concrete_camera_mixin_instance: CameraClientMixin,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        concrete_camera_mixin_instance.client,
        CameraClient,
    )
    assert concrete_camera_mixin_instance.log == mocked_task_logger
    assert concrete_camera_mixin_instance.client.log == mocked_task_logger
