"""Test the StepRenderConfiguration class."""
import logging
from io import StringIO
from unittest import mock

from pi_portal.installation.templates import common_templates
from ..step_render_configuration import StepRenderConfiguration


class TestStepRenderConfiguration:
  """Test the StepRenderConfiguration class."""

  def test__initialize__attrs(
      self,
      step_render_configuration_instance: StepRenderConfiguration,
  ) -> None:
    assert isinstance(step_render_configuration_instance.log, logging.Logger)
    assert step_render_configuration_instance.templates == common_templates

  def test__invoke__success__logging(
      self,
      step_render_configuration_instance: StepRenderConfiguration,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0

    step_render_configuration_instance.invoke()

    assert mocked_stream.getvalue() == (
        "test - INFO - Rendering configuration templates ...\n"
        "test - INFO - Done rendering configuration templates.\n"
    )

  def test__invoke__render_call(
      self,
      step_render_configuration_instance: StepRenderConfiguration,
      mocked_template_render: mock.Mock,
  ) -> None:
    step_render_configuration_instance.invoke()

    mocked_template_render.assert_called_once_with()
