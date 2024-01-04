"""StepKillMotion class."""

from .bases import service_step


class StepKillMotion(service_step.ServiceStepBase):
  """Kill the motion process and remove it from startup."""

  service = service_step.ServiceDefinition(
      service_name="motion",
      system_v_service_name="motion",
      systemd_unit_name="motion.service",
  )

  def invoke(self) -> None:
    """Kill the motion process and remove it from startup."""

    self.stop()
    self.disable()
