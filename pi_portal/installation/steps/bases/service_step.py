"""ServiceStepBase class."""
import abc
import dataclasses

from . import system_call_step


@dataclasses.dataclass
class ServiceDefinition:
  """A Linux service."""

  service_name: str
  system_v_service_name: str
  systemd_unit_name: str


class ServiceStepBase(system_call_step.SystemCallBase, abc.ABC):
  """Linux service management installer step."""

  service: ServiceDefinition

  def disable(self) -> None:
    """Disable the service."""

    self.log.info(
        "Service: attempting to disable the '%s' service ...",
        self.service.service_name,
    )

    if not self._disable_via_system_v():
      if not self._disable_via_systemd():
        self.log.warning(
            "Service: The '%s' service could not be disabled!",
            self.service.service_name,
        )
        self.log.warning(
            "Service: This service should be controlled by pi_portal!  "
            "Please disable it manually if required!"
        )
        return

    self.log.info(
        "Service: done attempting to disable the '%s' service.",
        self.service.service_name,
    )

  def enable(self) -> None:
    """Enable the service."""

    self.log.info(
        "Service: attempting to enable the '%s' service ...",
        self.service.service_name,
    )

    if not self._enable_via_system_v():
      if not self._enable_via_systemd():
        self.log.error(
            "Service: IMPORTANT! The '%s' service could not be enabled!",
            self.service.service_name
        )
        self.log.error("Service: Please enable and start it manually!")
        return

    self.log.info(
        "Service: done attempting to enable the '%s' service.",
        self.service.service_name,
    )

  def start(self) -> None:
    """Start the service."""

    self.log.info(
        "Service: attempting to start the '%s' service ...",
        self.service.service_name,
    )

    if not self._start_via_system_v():
      if not self._start_via_systemd():
        self.log.error(
            "Service: IMPORTANT! The '%s' service could not be started!",
            self.service.service_name
        )
        self.log.error("Service: Please start it manually!")

    self.log.info(
        "Service: done attempting to start the '%s' service.",
        self.service.service_name,
    )

  def stop(self) -> None:
    """Stop the service."""

    self.log.info(
        "Service: attempting to stop the '%s' service ...",
        self.service.service_name,
    )

    if not self._stop_via_system_v():
      if not self._stop_via_systemd():
        self.log.warning(
            "Service: The '%s' service does not appear to be running ...",
            self.service.service_name,
        )
        self.log.warning(
            "Service: It could be running via an unknown init system."
        )

    self.log.info(
        "Service: done attempting to stop the '%s' service.",
        self.service.service_name,
    )

  def _disable_via_system_v(self) -> bool:
    try:
      self._system_call(
          f"update-rc.d {self.service.system_v_service_name} disable"
      )
      return True
    except system_call_step.SystemCallError:
      self.log.warning(
          "Service: unable to disable '%s' via a System V service.",
          self.service.service_name,
      )
      return False

  def _disable_via_systemd(self) -> bool:
    try:
      self._system_call(f"systemctl disable {self.service.systemd_unit_name}")
      return True
    except system_call_step.SystemCallError:
      self.log.warning(
          "Service: unable to disable '%s' via systemd.",
          self.service.service_name,
      )
      return False

  def _enable_via_system_v(self) -> bool:
    try:
      self._system_call(
          f"update-rc.d {self.service.system_v_service_name} enable"
      )
      return True
    except system_call_step.SystemCallError:
      self.log.warning(
          "Service: unable to enable '%s' via a System V service.",
          self.service.service_name
      )
      return False

  def _enable_via_systemd(self) -> bool:
    try:
      self._system_call(f"systemctl enable {self.service.systemd_unit_name}")
      return True
    except system_call_step.SystemCallError:
      self.log.warning(
          "Service: unable to enable '%s' via systemd.",
          self.service.service_name,
      )
      return False

  def _start_via_system_v(self) -> bool:
    try:
      self._system_call(f"service {self.service.system_v_service_name} start")
      return True
    except system_call_step.SystemCallError:
      self.log.warning(
          "Service: '%s' could not be started via a System V service.",
          self.service.service_name,
      )
      return False

  def _start_via_systemd(self) -> bool:
    try:
      self._system_call(f"systemctl start {self.service.systemd_unit_name}")
      return True
    except system_call_step.SystemCallError:
      self.log.warning(
          "Service: '%s' could not be started via a systemd unit.",
          self.service.service_name,
      )
      return False

  def _stop_via_system_v(self) -> bool:
    try:
      self._system_call(f"service {self.service.system_v_service_name} stop")
      return True
    except system_call_step.SystemCallError:
      self.log.warning(
          "Service: '%s' is not running via a System V service.",
          self.service.service_name,
      )
      return False

  def _stop_via_systemd(self) -> bool:
    try:
      self._system_call(f"systemctl stop {self.service.systemd_unit_name}")
      return True
    except system_call_step.SystemCallError:
      self.log.warning(
          "Service: '%s' is not running via a systemd unit.",
          self.service.service_name,
      )
      return False
