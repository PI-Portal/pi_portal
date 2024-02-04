"""An archival client for archival task processors."""

from pi_portal.modules.integrations.s3 import client as s3_client


class ArchivalClientMixin:
  """An archival client for archival task processors."""

  archival_client_class = s3_client.S3BucketClient
  archival_client_exception_class = s3_client.S3BucketException
