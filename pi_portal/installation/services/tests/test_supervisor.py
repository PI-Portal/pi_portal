"""Test the supervisor service definition."""
from .. import supervisor


class TestSupervisorServiceDefinition:
  """Test the supervisor service definition."""

  def test_attributes(self,) -> None:
    assert supervisor.supervisor_service.service_name == "supervisor"
    assert supervisor.supervisor_service.system_v_service_name == "supervisor"
    assert supervisor.supervisor_service.systemd_unit_name == (
        "supervisor.service"
    )
