"""Test the ArchivalClientMixin class."""

from pi_portal.modules.integrations.s3 import client as s3_client
from pi_portal.modules.tasks.processor.mixins.archival_client import (
    ArchivalClientMixin,
)


class TestArchivalClientMixin:
  """Test the ArchivalClientMixin class."""

  def test_initialize__archival_client(
      self,
      concrete_archival_mixin_instance: ArchivalClientMixin,
  ) -> None:
    assert concrete_archival_mixin_instance.archival_client_class == \
        s3_client.S3BucketClient
    assert concrete_archival_mixin_instance.archival_client_exception_class == \
        s3_client.S3BucketException
