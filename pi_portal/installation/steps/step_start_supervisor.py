"""StepStartSupervisor class."""

from .bases import service_step


class StepStartSupervisor(service_step.ServiceStepBase):
  """Start the supervisor process and add it to startup."""

  service = service_step.ServiceDefinition(
      service_name="supervisor",
      system_v_service_name="supervisor",
      systemd_unit_name="supervisor.service",
  )

  def invoke(self) -> None:
    """Start the supervisor process and add it to startup."""

    self.enable()
    self.start()
