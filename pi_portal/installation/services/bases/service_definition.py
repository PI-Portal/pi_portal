"""ServiceDefinition class."""

import dataclasses


@dataclasses.dataclass
class ServiceDefinition:
  """Definition of a linux service across multiple distros."""

  service_name: str
  system_v_service_name: str
  systemd_unit_name: str
