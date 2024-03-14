"""Test the StepConfigureLogzIo class."""

from ...utility.generate_step_test import GenericStepTest
from .. import (
    StepConfigureLogzIo,
    action_create_paths,
    action_remote_files,
    action_render_templates,
)


class TestStepConfigureLogzIo(GenericStepTest):
  """Test the StepConfigureLogzIo class."""

  step_class = StepConfigureLogzIo
  action_classes = [
      action_create_paths.CreateLogzIoPathsAction,
      action_remote_files.RemoteFileLogzIoAction,
      action_render_templates.RenderLogIoTemplates,
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Configuring the logz.io integration ..."
    )
    assert self.step_class.logging_end_message == (
        "Done configuring the logz.io integration."
    )
