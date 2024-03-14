"""StepStopSupervisordService class."""

from ..bases import base_step
from . import action_supervisord_service_stop


class StepStopSupervisordService(base_step.StepBase):
  """Stop the supervisord service."""

  actions = [
      action_supervisord_service_stop.StopSupervisordServiceAction,
  ]
  logging_begin_message = "Stopping the supervisord service ..."
  logging_end_message = "Done stopping the supervisord service."
