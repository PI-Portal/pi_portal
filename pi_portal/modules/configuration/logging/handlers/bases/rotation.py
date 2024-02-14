"""RotatingFileHandlerBase class."""

from logging.handlers import RotatingFileHandler


class RotatingFileHandlerBase(RotatingFileHandler):
  """Rotating file handler base class."""

  def __init__(self, filename: str):
    super().__init__(
        filename,
        backupCount=3,
        delay=True,
        encoding="utf-8",
        maxBytes=10000000,  # 10MB
    )
