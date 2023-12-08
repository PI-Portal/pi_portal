"""Test the StepEnsureRoot class."""
import logging
import os
from io import StringIO
from unittest import mock

import pytest
from .. import step_ensure_root


class TestStepEnsureRoot:
  """Test the StepEnsureRoot class."""

  def test__initialize__attrs(
      self,
      step_ensure_root_instance: step_ensure_root.StepEnsureRoot,
  ) -> None:
    assert isinstance(step_ensure_root_instance.log, logging.Logger)

  def test__invoke__is_root(
      self,
      step_ensure_root_instance: step_ensure_root.StepEnsureRoot,
      mocked_stream: StringIO,
  ) -> None:
    with mock.patch.object(os, "geteuid", return_value=0):
      step_ensure_root_instance.invoke()

    assert mocked_stream.getvalue() == \
        (
          "test - INFO - Ensuring that the installer is running as root ...\n"
          "test - INFO - Done ensuring that the installer is running as root.\n"
        )

  def test__invoke__is_not_root(
      self,
      step_ensure_root_instance: step_ensure_root.StepEnsureRoot,
      mocked_stream: StringIO,
  ) -> None:
    with mock.patch.object(os, "geteuid", return_value=1000):
      with pytest.raises(PermissionError) as exc:

        step_ensure_root_instance.invoke()

    assert str(exc.value) == \
        step_ensure_root_instance.insufficient_privileges_msg

    assert mocked_stream.getvalue() == \
        (
           "test - INFO - Ensuring that the installer is running as root ...\n"
           "test - ERROR - This installer must be run as root!\n"
        )
