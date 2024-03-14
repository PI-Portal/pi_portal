"""Test the RenderTemplatesAction class."""

import logging
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal.installation.templates import config_file
from pi_portal.modules.python.mock import CallType
from ..action_render_templates import RenderTemplatesAction
from ..bases import base_action


class TestRenderTemplatesAction:
  """Test the RenderTemplatesAction class."""

  def build_logging__successful(
      self,
      templates: List[config_file.ConfileFileTemplate],
  ) -> str:
    expected_logging_messages = ""
    for template in templates:
      expected_logging_messages += "\n".join(
          [
              (
                  f"INFO - Template: '{template.source}' -> "
                  f"'{template.destination}' ..."
              ),
              (
                  f"INFO - Template: '{template.source}' -> "
                  f"'{template.destination}' completed."
              ),
          ]
      ) + "\n"
    return expected_logging_messages

  def build_logging__file_system_call_failed(
      self,
      templates: List[config_file.ConfileFileTemplate],
  ) -> str:
    expected_log_calls = ""
    for template in templates:
      expected_log_calls += "\n".join(
          [
              (
                  f"INFO - Template: '{template.source}' -> "
                  f"'{template.destination}' ..."
              ),
          ]
      ) + "\n"
    return expected_log_calls

  def build_mocked_file_system_calls(
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

  def test_initialize__attributes(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
  ) -> None:
    assert isinstance(
        concrete_templates_render_action_instance.log,
        logging.Logger,
    )

  def test_initialize__inheritance(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
  ) -> None:
    assert isinstance(
        concrete_templates_render_action_instance,
        base_action.ActionBase,
    )

  def test_initialize__templates(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
  ) -> None:
    assert len(concrete_templates_render_action_instance.templates) == 2
    for templated_file in concrete_templates_render_action_instance.templates:
      assert isinstance(templated_file, config_file.ConfileFileTemplate)

  def test_invoke__success__logging(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = self.build_logging__successful(
        concrete_templates_render_action_instance.templates
    )

    concrete_templates_render_action_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  def test_invoke__success__file_system_calls(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
      mocked_file_system: mock.Mock,
  ) -> None:
    expected_fs_calls = self.build_mocked_file_system_calls(
        concrete_templates_render_action_instance.templates
    )

    concrete_templates_render_action_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls

  def test_invoke__success__template_rendering_calls(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
      mocked_template_render: mock.Mock,
  ) -> None:
    concrete_templates_render_action_instance.invoke()

    assert mocked_template_render.mock_calls == [
        mock.call(),
    ] * len(concrete_templates_render_action_instance.templates)

  def test_invoke__file_system_failure__logging(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError
    expected_log_messages = \
        self.build_logging__file_system_call_failed(
            concrete_templates_render_action_instance.templates[0:1]
        )

    with pytest.raises(OSError):
      concrete_templates_render_action_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  def test_invoke__file_system_failure__file_system_calls(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
      mocked_file_system: mock.Mock,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError
    expected_fs_calls = self.build_mocked_file_system_calls(
        concrete_templates_render_action_instance.templates[0:1]
    )

    with pytest.raises(OSError):
      concrete_templates_render_action_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls

  def test_invoke__file_system_failure__template_rendering_calls(
      self,
      concrete_templates_render_action_instance: RenderTemplatesAction,
      mocked_file_system: mock.Mock,
      mocked_template_render: mock.Mock,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError

    with pytest.raises(OSError):
      concrete_templates_render_action_instance.invoke()

    assert mocked_template_render.mock_calls == [mock.call()]
