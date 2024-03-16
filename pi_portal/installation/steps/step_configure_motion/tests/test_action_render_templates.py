"""Test the RenderMotionTemplatesAction class."""

from io import StringIO
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.configuration import state
from ...utility.generate_action_render_templates_test import (
    GenericRenderTemplatesActionTest,
)
from ..action_render_templates import RenderMotionTemplatesAction


@pytest.mark.usefixtures("test_state")
class TestRenderMotionTemplatesAction(GenericRenderTemplatesActionTest):
  """Test the RenderMotionTemplatesAction class."""

  action_class = RenderMotionTemplatesAction

  def test_initialize__attributes__templates(self) -> None:
    assert len(self.action_class.templates) == 1

  def test_initialize__attributes__motion_config(self) -> None:
    motion_config = self.action_class.templates[0]
    assert motion_config.source == "motion/motion.conf"
    assert motion_config.destination == config.PATH_CAMERA_CONFIG
    assert motion_config.permissions == "600"
    assert motion_config.user == config.PI_PORTAL_USER
    assert motion_config.group == config.PI_PORTAL_USER

  def test_invoke__generates_camera_templates_before_rendering(
      self,
      render_motion_templates_action_instance: RenderMotionTemplatesAction,
      render_motion_templates_action_sequence: mock.Mock,
  ) -> None:

    render_motion_templates_action_instance.invoke()

    assert render_motion_templates_action_sequence.mock_calls == [
        mock.call.generate_camera_templates(),
        mock.call.super_invoke()
    ]

  def test_invoke__success__logging(
      self,
      render_motion_templates_action_instance: RenderMotionTemplatesAction,
      test_state: state.State,
      mocked_stream: StringIO,
  ) -> None:
    camera_config = test_state.user_config["CAMERA"]["MOTION"]["CAMERAS"]

    render_motion_templates_action_instance.invoke()

    assert mocked_stream.getvalue() == "".join(
        [
            f"INFO - Creating template for '{camera['DEVICE']}' ...\n"
            for camera in camera_config
        ]
    )

  def test_generate_camera_templates__updates_templates(
      self,
      render_motion_templates_action_instance: RenderMotionTemplatesAction,
      test_state: state.State,
  ) -> None:
    camera_config = test_state.user_config["CAMERA"]["MOTION"]["CAMERAS"]
    motion_template_count = len(
        render_motion_templates_action_instance.templates
    )
    assert len(render_motion_templates_action_instance.templates) == 1

    render_motion_templates_action_instance.generate_camera_templates()

    assert len(render_motion_templates_action_instance.templates) == \
        motion_template_count + len(camera_config)

  def test_generate_camera_templates__creates_valid_templates(
      self,
      render_motion_templates_action_instance: RenderMotionTemplatesAction,
      test_state: state.State,
  ) -> None:
    camera_config = test_state.user_config["CAMERA"]["MOTION"]["CAMERAS"]

    render_motion_templates_action_instance.generate_camera_templates()

    camera_templates = render_motion_templates_action_instance.templates[1:]
    for index0, template in enumerate(camera_templates):
      index = index0 + 1
      assert template.source == "motion/camera.conf"
      assert template.destination == f'/etc/motion/camera{index}.conf'
      assert template.permissions == "600"
      assert template.user == config.PI_PORTAL_USER
      assert template.context["CAMERA"] == camera_config[index0]
      assert template.context["CAMERA"]["NAME"] == f"CAMERA-{index}"
      assert template.context["CAMERA"]["ID"] == index
