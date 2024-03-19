"""Test the flags monostate."""

from unittest import mock

from .. import flags


class TestFlags:
  """Test the flags default values."""

  def test_instantiate__attributes(
      self,
      flags_instance: flags.Flags,
  ) -> None:
    assert flags_instance.FLAG_CAMERA_DISABLED_BY_CRON is False


class TestFlagState:
  """Test the flags monostate."""

  def test_instantiate__attributes(
      self,
      flag_state_instance: flags.FlagState,
      mocked_flags: mock.Mock,
  ) -> None:
    assert flag_state_instance.flags == mocked_flags.return_value

  def test_instantiate__mono_state__flags_are_shared(
      self,
      flag_state_instance: flags.FlagState,
      flag_state_instance_clone: flags.FlagState,
  ) -> None:
    flag_state_instance.flags.FLAG_CAMERA_DISABLED_BY_CRON = (
        not flag_state_instance.flags.FLAG_CAMERA_DISABLED_BY_CRON
    )

    assert flag_state_instance.flags.FLAG_CAMERA_DISABLED_BY_CRON == (
        flag_state_instance_clone.flags.FLAG_CAMERA_DISABLED_BY_CRON
    )
