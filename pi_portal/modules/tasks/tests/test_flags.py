"""Test the Flags class."""

from .. import flags


class TestFlags:
  """Test the Flags class."""

  def test_instantiate__attributes(
      self,
      flags_instance: flags.Flags,
  ) -> None:
    assert flags_instance.FLAG_CAMERA_DISABLED_BY_CRON is False
