"""Test the StepRenderConfiguration class."""
import logging
import os
from io import StringIO
from unittest import mock

from pi_portal.installation.templates import config_file, motion_templates
from pi_portal.modules.configuration import state
from ..step_configure_motion import StepConfigureMotion


class TestStepRenderTemplates:
  """Test the StepRenderConfiguration class."""

  def test__initialize__attrs(
      self,
      step_configure_motion_instance: StepConfigureMotion,
  ) -> None:
    assert isinstance(step_configure_motion_instance.log, logging.Logger)
    assert step_configure_motion_instance.templates == motion_templates

  def test__invoke__success__logging(
      self,
      step_configure_motion_instance: StepConfigureMotion,
      mocked_state: state.State,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    camera_config = mocked_state.user_config["MOTION"]["CAMERAS"]
    expected_log_messages = ""
    for camera in camera_config:
      expected_log_messages += \
          f"test - INFO - Creating template for '{camera['DEVICE']}' ...\n"

    step_configure_motion_instance.invoke()

    assert mocked_stream.getvalue() == (
        "test - INFO - Rendering motion configuration ...\n" +
        expected_log_messages +
        "test - INFO - Done rendering motion configuration.\n"
    )

  def test__invoke__render_call(
      self,
      step_configure_motion_instance: StepConfigureMotion,
      mocked_template_render: mock.Mock,
  ) -> None:
    step_configure_motion_instance.invoke()

    mocked_template_render.assert_called_once_with()

  def test__generate_camera_templates__updates_templates(
      self,
      step_configure_motion_instance: StepConfigureMotion,
      mocked_state: state.State,
  ) -> None:
    camera_config = mocked_state.user_config["MOTION"]["CAMERAS"]
    motion_template_count = len(motion_templates)
    assert step_configure_motion_instance.templates == \
           motion_templates

    step_configure_motion_instance.generate_camera_templates()

    assert len(step_configure_motion_instance.templates) == \
           motion_template_count + len(camera_config)

  def test__generate_camera_templates__creates_valid_templates(
      self,
      step_configure_motion_instance: StepConfigureMotion,
      mocked_state: state.State,
  ) -> None:
    camera_config = mocked_state.user_config["MOTION"]["CAMERAS"]
    motion_template_count = len(motion_templates)

    step_configure_motion_instance.generate_camera_templates()

    camera_templates = step_configure_motion_instance.\
        templates[motion_template_count:]
    for index0, template in enumerate(camera_templates):
      index = index0 + 1
      assert template.source == os.path.join(
          os.path.dirname(config_file.__file__),
          "motion/camera.conf",
      )
      assert template.destination == f'/etc/motion/camera{index}.conf'
      assert template.permissions == "600"
      assert template.user == "root"
      assert template.context["CAMERA"] == camera_config[index0]
      assert template.context["CAMERA"]["NAME"] == f"CAMERA-{index}"
      assert template.context["CAMERA"]["ID"] == index
