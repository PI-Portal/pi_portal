"""StepKillSupervisor class."""

from .bases import service_step


class StepKillSupervisor(service_step.ServiceStepBase):
  """Kill the supervisor process."""

  service = service_step.ServiceDefinition(
      service_name="supervisor",
      system_v_service_name="supervisor",
      systemd_unit_name="supervisor.service",
  )

  def invoke(self) -> None:
    """Kill the supervisor process."""

    self.stop()
