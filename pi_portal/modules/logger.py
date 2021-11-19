"""Logger configuration."""

import logging
import uuid

LOG_UUID = str(uuid.uuid4())

LOG_FORMATTER = logging.Formatter(
    "%(asctime)s [ " + LOG_UUID + " ] [ %(levelname)s ] %(message)s"
)


def setup_logger(log: logging.Logger, fname: str) -> logging.Logger:
  """Configure application logging.

  :param log: The logger instance to configure.
  :param fname: The path to write logs to.

  :returns: The configured logger instance.
  """

  log.setLevel(logging.DEBUG)
  log.handlers = []
  handler = logging.FileHandler(fname, delay=True)
  handler.setFormatter(LOG_FORMATTER)
  log.addHandler(handler)
  return log
