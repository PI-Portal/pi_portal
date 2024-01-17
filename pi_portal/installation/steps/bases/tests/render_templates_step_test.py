"""Test the RenderTemplateStepBase class."""

import logging
import os
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal.installation.templates import config_file
from pi_portal.modules.python.mock import CallType
from .. import base_step
from ..render_templates_step import RenderTemplateStepBase


class TestRenderTemplateStepBase:
  """Test the RenderTemplateStepBase class."""

  def build_log_messages(
      self,
      templates: List[config_file.ConfileFileTemplate],
  ) -> str:
    expected_log_calls = ""
    for template in templates:
      expected_log_calls += "\n".join(
          [
              (
                  f"test - INFO - Template: '{template.source}' -> "
                  f"'{template.destination}' ..."
              ),
              (
                  f"test - INFO - Template: '{template.source}' -> "
                  f"'{template.destination}' completed."
              ),
          ]
      ) + "\n"
    return expected_log_calls

  def build_fs_call_failed_log_messages(
      self,
      templates: List[config_file.ConfileFileTemplate],
  ) -> str:
    expected_log_calls = ""
    for template in templates:
      expected_log_calls += "\n".join(
          [
              (
                  f"test - INFO - Template: '{template.source}' -> "
                  f"'{template.destination}' ..."
              ),
          ]
      ) + "\n"
    return expected_log_calls

  def build_mocked_fs_calls(
      self,
      templates: List[config_file.ConfileFileTemplate],
  ) -> List[CallType]:
    expected_fs_calls: List[CallType] = []
    for template in templates:
      expected_fs_calls += [
          mock.call(template.destination),
          mock.call().ownership(template.user, template.user),
          mock.call().permissions(template.permissions),
      ]
    return expected_fs_calls

  def test__initialize__attrs(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
  ) -> None:
    assert isinstance(
        concrete_render_templates_step_instance.log,
        logging.Logger,
    )

  def test__initialize__inheritance(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
  ) -> None:
    assert isinstance(
        concrete_render_templates_step_instance,
        base_step.StepBase,
    )

  def test__initialize__templates(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
  ) -> None:
    assert len(concrete_render_templates_step_instance.templates) == 2

    file1 = concrete_render_templates_step_instance.templates[0]
    assert isinstance(file1, config_file.ConfileFileTemplate)
    assert file1.source == os.path.join(
        os.path.dirname(config_file.__file__),
        "templates/file1",
    )
    assert file1.destination == "/etc/file1"
    assert file1.permissions == "600"
    assert file1.user == "root"

    file2 = concrete_render_templates_step_instance.templates[1]
    assert isinstance(file2, config_file.ConfileFileTemplate)
    assert file2.source == os.path.join(
        os.path.dirname(config_file.__file__),
        "templates/file2",
    )
    assert file2.destination == "/etc/file2"
    assert file2.permissions == "755"
    assert file2.user == "test_user"

  def test__render__logs__success(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = self.build_log_messages(
        concrete_render_templates_step_instance.templates
    )

    concrete_render_templates_step_instance.render()

    assert mocked_stream.getvalue() == expected_log_messages

  def test__render__logs__fs_failure(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError
    expected_log_messages = \
        self.build_fs_call_failed_log_messages(
            concrete_render_templates_step_instance.templates[0:1]
        )

    with pytest.raises(OSError):
      concrete_render_templates_step_instance.render()

    assert mocked_stream.getvalue() == expected_log_messages

  def test__render__fs_calls__success(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
      mocked_file_system: mock.Mock,
  ) -> None:
    expected_fs_calls = self.build_mocked_fs_calls(
        concrete_render_templates_step_instance.templates
    )

    concrete_render_templates_step_instance.render()

    assert mocked_file_system.mock_calls == expected_fs_calls

  def test__render__fs__calls__fs_call_failure(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
      mocked_file_system: mock.Mock,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError
    expected_fs_calls = self.build_mocked_fs_calls(
        concrete_render_templates_step_instance.templates[0:1]
    )

    with pytest.raises(OSError):
      concrete_render_templates_step_instance.render()

    assert mocked_file_system.mock_calls == expected_fs_calls

  def test__render__template_rendering__success(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
      mocked_template_render: mock.Mock,
  ) -> None:
    concrete_render_templates_step_instance.render()

    assert mocked_template_render.mock_calls == [
        mock.call(),
    ] * len(concrete_render_templates_step_instance.templates)

  def test__render__template_rendering__fs_failure(
      self,
      concrete_render_templates_step_instance: RenderTemplateStepBase,
      mocked_file_system: mock.Mock,
      mocked_template_render: mock.Mock,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError

    with pytest.raises(OSError):
      concrete_render_templates_step_instance.render()

    assert mocked_template_render.mock_calls == [mock.call()]
