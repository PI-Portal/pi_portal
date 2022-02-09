"""Logger configuration."""

import logging

from pi_portal.modules.configuration import state


class LoggingConfiguration:
  """Pi Portal logging configuration."""

  def __init__(self) -> None:
    running_state = state.State()
    self.level = running_state.log_level
    self.formatter = logging.Formatter(
        "%(asctime)s [ " + running_state.log_uuid +
        " ] [ %(levelname)s ] %(message)s"
    )

  def configure(self, log: logging.Logger, fname: str) -> logging.Logger:
    """Configure application logging.

    :param log: The logger instance to configure.
    :param fname: The path to write logs to.

    :returns: The configured logger instance.
    """

    log.setLevel(self.level)
    log.handlers = []
    handler = logging.FileHandler(fname, delay=True)
    handler.setFormatter(self.formatter)
    log.addHandler(handler)
    return log
