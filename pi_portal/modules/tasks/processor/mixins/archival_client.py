"""An archival client for archival task processors."""

from typing import Type

from pi_portal.modules.integrations.archival import (
    ArchivalException,
    TypeArchivalClient,
)
from pi_portal.modules.integrations.archival.service_client import (
    ArchivalClient,
)


class ArchivalClientMixin:
  """An archival client for archival task processors."""

  archival_client_class: Type[TypeArchivalClient] = ArchivalClient
  archival_client_exception_class: Type[Exception] = ArchivalException
