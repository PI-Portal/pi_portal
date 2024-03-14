"""Test the motion service definition."""
from .. import motion


class TestMotionServiceDefinition:
  """Test the motion service definition."""

  def test_attributes(self,) -> None:
    assert motion.motion_service.service_name == "motion"
    assert motion.motion_service.system_v_service_name == "motion"
    assert motion.motion_service.systemd_unit_name == "motion.service"
