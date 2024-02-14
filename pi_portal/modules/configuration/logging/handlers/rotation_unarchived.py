"""RotatingFileHandlerUnarchived class."""

from .bases.rotation import RotatingFileHandlerBase


class RotatingFileHandlerUnarchived(RotatingFileHandlerBase):
  """Rotating file handler without archival processing."""
