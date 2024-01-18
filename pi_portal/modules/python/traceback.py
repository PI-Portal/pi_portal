"""Traceback related utilities."""
import traceback
from dataclasses import dataclass
from typing import Optional


@dataclass
class CapturedException:
  """A captured exception that was raised."""

  exception: Optional[Exception] = None
  traceback: str = ""


def get_traceback(exc: Exception) -> str:
  """Generate a traceback messages from a raised exception.

  :param exc: The exception to extract the traceback from.
  :returns: The string output of the traceback.
  """
  output = ""
  output += "".join(
      traceback.format_exception(
          type(exc),
          value=exc,
          tb=exc.__traceback__,
      ),
  )

  return output
