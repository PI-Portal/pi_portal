"""Fixtures for the step_configure_motion action classes tests."""
# pylint: disable=redefined-outer-name
import logging
from copy import deepcopy
from unittest import mock

import pytest
from .. import action_render_templates


@pytest.fixture
def mocked_super_invoke() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def render_motion_templates_action_instance(
    installer_logger_stdout: logging.Logger,
    mocked_super_invoke: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> action_render_templates.RenderMotionTemplatesAction:
  monkeypatch.setattr(
      action_render_templates.__name__ + ".RenderTemplatesAction.invoke",
      mocked_super_invoke
  )

  class ClonedAction(action_render_templates.RenderMotionTemplatesAction):
    """Preserve the original set of templates for testing."""

    templates = deepcopy(
        action_render_templates.RenderMotionTemplatesAction.templates
    )

  return ClonedAction(installer_logger_stdout)


@pytest.fixture
def render_motion_templates_action_sequence(
    mocked_super_invoke: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> mock.Mock:
  sequence = mock.Mock()
  mocked_generate_camera_templates = mock.Mock(name="generate_camera_templates")
  mocked_super_invoke.name = 'super_invoke'
  sequence.attach_mock(
      mocked_generate_camera_templates,
      "generate_camera_templates",
  )
  sequence.attach_mock(
      mocked_super_invoke,
      "super_invoke",
  )

  monkeypatch.setattr(
      action_render_templates.__name__ +
      ".RenderMotionTemplatesAction.generate_camera_templates",
      mocked_generate_camera_templates
  )

  return sequence
