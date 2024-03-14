"""The motion service definition."""

from .bases import service_definition

motion_service = service_definition.ServiceDefinition(
    service_name="motion",
    system_v_service_name="motion",
    systemd_unit_name="motion.service",
)
