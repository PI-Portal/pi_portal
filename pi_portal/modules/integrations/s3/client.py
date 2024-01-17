"""S3BucketClient class."""

import boto3
from botocore.exceptions import ClientError
from pi_portal.modules.configuration import state


class S3BucketException(Exception):
  """Exception for S3 Bucket errors."""


class S3BucketClient:
  """S3BucketClient class."""

  def __init__(self, bucket_name: str) -> None:
    current_state = state.State()
    self.bucket_name = bucket_name
    self.boto_client = boto3.client(
        's3',
        aws_access_key_id=current_state.user_config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_state.
        user_config['AWS_SECRET_ACCESS_KEY'],
    )

  def upload(
      self,
      file_name: str,
      object_name: str,
  ) -> None:
    """Upload the specified file to the S3 bucket.

    :param file_name: The path of the file to upload.
    :param object_name: The name of the S3 object that will be created.
    :raises: :class:`S3BucketException`
    """

    try:
      self.boto_client.upload_file(
          file_name,
          self.bucket_name,
          object_name,
      )
    except ClientError as exc:
      raise S3BucketException from exc
