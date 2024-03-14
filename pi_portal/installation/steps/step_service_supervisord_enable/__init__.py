"""StepEnableSupervisordService class."""

from ..bases import base_step
from . import (
    action_supervisord_service_enable,
    action_supervisord_service_start,
)


class StepEnableSupervisordService(base_step.StepBase):
  """Manage the default motion service."""

  actions = [
      action_supervisord_service_start.StartSupervisordServiceAction,
      action_supervisord_service_enable.EnableSupervisordServiceAction
  ]
  logging_begin_message = "Enabling the supervisord service ..."
  logging_end_message = "Done enabling the supervisord service."
