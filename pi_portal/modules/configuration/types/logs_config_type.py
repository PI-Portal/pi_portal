"""Logs configuration types."""

from typing_extensions import TypedDict


class TypeUserConfigLogs(TypedDict):
  """Typed representation of the logs configuration."""

  LOGZ_IO: "TypeUserConfigLogsLogzIO"


class TypeUserConfigLogsLogzIO(TypedDict):
  """Typed representation of the LogzIO logs configuration."""

  LOGZ_IO_TOKEN: str
