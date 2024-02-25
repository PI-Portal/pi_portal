"""AWS archival client implementation."""

import boto3
from botocore.exceptions import ClientError
from pi_portal.modules.integrations.archival.bases.client import (
    ArchivalClientBase,
    ArchivalException,
)


class S3BucketClient(ArchivalClientBase):
  """S3BucketClient class.

  :param bucket_name: The name of the S3 bucket to use.
  """

  def __init__(self, bucket_name: str) -> None:
    super().__init__(bucket_name)
    aws_config = self.current_state.user_config["ARCHIVAL"]["AWS"]
    self.boto_client = boto3.client(
        's3',
        aws_access_key_id=aws_config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=aws_config['AWS_SECRET_ACCESS_KEY'],
    )

  def upload(
      self,
      local_file_name: str,
      archival_file_name: str,
  ) -> None:
    """Upload the specified file to the S3 bucket.

    :param local_file_name: The path of the file to upload.
    :param archival_file_name: The name of the S3 object that will be created.
    :raises: :class:`ArchivalException`
    """

    try:
      self.boto_client.upload_file(
          local_file_name,
          self.partition_name,
          archival_file_name,
      )
    except ClientError as exc:
      raise ArchivalException from exc
