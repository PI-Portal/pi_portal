"""S3 Integration class."""

import boto3
import pi_portal
from botocore.exceptions import ClientError


class S3BucketException(Exception):
  """Exception for S3 Bucket errors."""


class S3Bucket:
  """S3 integration class."""

  def __init__(self):
    self.bucket_name = pi_portal.user_config['S3_BUCKET_NAME']
    self.boto_client = boto3.client('s3')

  def upload(self, file_name: str):
    """Upload the specified file to the S3 bucket."""

    try:
      self.boto_client.upload_file(file_name, self.bucket_name, file_name)
    except ClientError as exc:
      raise S3BucketException from exc
