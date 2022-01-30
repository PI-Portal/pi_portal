"""S3 Integration class."""

import os

import boto3
from botocore.exceptions import ClientError
from pi_portal.modules.configuration import state


class S3BucketException(Exception):
  """Exception for S3 Bucket errors."""


class S3Bucket:
  """S3 integration class."""

  def __init__(self):
    current_state = state.State()
    self.bucket_name = current_state.user_config['S3_BUCKET_NAME']
    self.boto_client = boto3.client(
        's3',
        aws_access_key_id=current_state.user_config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_state.
        user_config['AWS_SECRET_ACCESS_KEY'],
    )

  def upload(self, file_name: str):
    """Upload the specified file to the S3 bucket.

    :param file_name: The path of the file to upload.
    """

    try:
      self.boto_client.upload_file(
          file_name, self.bucket_name, os.path.basename(file_name)
      )
    except ClientError as exc:
      raise S3BucketException from exc
