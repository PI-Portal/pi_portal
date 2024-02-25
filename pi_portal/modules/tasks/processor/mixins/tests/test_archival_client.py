"""Test the ArchivalClientMixin class."""

import pytest
from pi_portal.modules.integrations.archival import ArchivalException
from pi_portal.modules.integrations.archival.service_client import (
    ArchivalClient,
)
from pi_portal.modules.tasks.processor.mixins.archival_client import (
    ArchivalClientMixin,
)


@pytest.mark.usefixtures('test_state')
class TestArchivalClientMixin:
  """Test the ArchivalClientMixin class."""

  def test_initialize__archival_client(
      self,
      concrete_archival_mixin_instance: ArchivalClientMixin,
  ) -> None:
    assert concrete_archival_mixin_instance.archival_client_class == (
        ArchivalClient
    )
    assert concrete_archival_mixin_instance.archival_client_exception_class == (
        ArchivalException
    )
