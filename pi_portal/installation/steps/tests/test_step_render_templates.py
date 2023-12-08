"""Test the StepRenderTemplates class."""
import logging
from io import StringIO
from typing import Iterator, List
from unittest import mock

import pytest
from pi_portal.installation.templates import (
    config_file,
    configuration_templates,
)
from pi_portal.modules.python.mock import CallType
from ..bases import system_call_step
from ..step_render_templates import StepRenderTemplates


class TestStepRenderTemplates:
  """Test the StepRenderTemplates class."""

  def build_success_log_arguments(
      self,
      template: config_file.ConfileFileTemplate,
  ) -> str:
    return "\n".join(
        [
            f"test - INFO - Template '{template.source}' -> "
            f"'{template.destination}' ...",
            "test - INFO - Executing: 'chown root:root "
            f"{template.destination}' ...",
            "test - INFO - Executing: 'chmod 600 "
            f"{template.destination}' ...",
            f"test - INFO - Completed '{template.source}' -> "
            f"'{template.destination}'."
        ]
    ) + "\n"

  def build_system_call_arguments(
      self,
      template: config_file.ConfileFileTemplate,
  ) -> Iterator[CallType]:
    return map(
        mock.call, [
            f"chown root:root {template.destination}",
            f"chmod 600 {template.destination}",
        ]
    )

  def test__initialize__attrs(
      self,
      step_render_templates_instance: StepRenderTemplates,
  ) -> None:
    assert isinstance(step_render_templates_instance.log, logging.Logger)
    assert step_render_templates_instance.templates == configuration_templates

  def test__invoke__success(
      self,
      step_render_templates_instance: StepRenderTemplates,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      mocked_template_render: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_log_messages = ""
    expected_system_calls: List[CallType] = []
    for template in configuration_templates:
      expected_log_messages += self.build_success_log_arguments(template)
      expected_system_calls += self.build_system_call_arguments(template)

    step_render_templates_instance.invoke()

    assert mocked_stream.getvalue() == \
        (
          "test - INFO - Rendering templates ...\n" +
          expected_log_messages +
          "test - INFO - Done rendering templates.\n"
        )
    assert mocked_system.mock_calls == expected_system_calls
    assert mocked_template_render.mock_calls == [
        mock.call()
    ] * len(configuration_templates)

  def test__invoke__failure(
      self,
      step_render_templates_instance: StepRenderTemplates,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      mocked_template_render: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0, 127]
    expected_log_messages = ""
    expected_system_calls: List[CallType] = []
    for template in configuration_templates[0:1]:
      expected_log_messages += self.build_success_log_arguments(template)
      expected_system_calls += self.build_system_call_arguments(template)

    with pytest.raises(system_call_step.SystemCallError) as exc:
      step_render_templates_instance.invoke()

    assert mocked_stream.getvalue() == \
           (
               "test - INFO - Rendering templates ...\n" +
               "\n".join(expected_log_messages.split("\n")[:-2]) + "\n" +
               "test - ERROR - Command: "
               "'chmod 600 /etc/filebeat/filebeat.yml' failed!\n"
           )
    assert mocked_system.mock_calls == expected_system_calls
    assert mocked_template_render.mock_calls == [mock.call()]
    assert str(exc.value) == \
        f"Command: 'chmod 600 {configuration_templates[0].destination}' " \
        "failed!"
