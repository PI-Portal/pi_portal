"""The motion service definition."""

from .bases import service_definition

supervisor_service = service_definition.ServiceDefinition(
    service_name="supervisor",
    system_v_service_name="supervisor",
    systemd_unit_name="supervisor.service",
)
