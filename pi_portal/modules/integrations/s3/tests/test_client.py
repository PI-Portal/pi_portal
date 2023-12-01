"""Test the S3BucketClient class."""

import os
from unittest import mock

import pytest
from botocore.exceptions import ClientError
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.s3 import client


class TestS3Bucket:
  """Test the S3BucketClient class."""

  def test__initialization__attrs(
      self,
      s3_client_instance: client.S3BucketClient,
      mocked_boto: mock.Mock,
  ) -> None:
    assert s3_client_instance.bucket_name == mock_state.MOCK_S3_BUCKET_NAME
    assert s3_client_instance.boto_client == mocked_boto.client.return_value

  def test__initialization__boto_client(
      self,
      # pylint: disable=unused-argument
      s3_client_instance: client.S3BucketClient,
      mocked_boto: mock.Mock,
  ) -> None:
    mocked_boto.client.assert_called_once_with(
        's3',
        aws_access_key_id=mock_state.MOCK_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=mock_state.MOCK_AWS_SECRET_ACCESS_KEY,
    )

  def test__upload__success(
      self,
      s3_client_instance: client.S3BucketClient,
  ) -> None:
    mock_file_name = "/dir/mock_file_name.mp4"

    s3_client_instance.upload(mock_file_name)

    s3_client_instance.boto_client.upload_file.assert_called_once_with(
        mock_file_name,
        s3_client_instance.bucket_name,
        os.path.basename(mock_file_name),
    )

  def test__upload__exception(
      self,
      s3_client_instance: client.S3BucketClient,
  ) -> None:
    s3_client_instance.boto_client.upload_file.side_effect = ClientError(
        error_response={},
        operation_name="BOOM!",
    )
    mock_file_name = "/dir/mock_file_name.mp4"

    with pytest.raises(client.S3BucketException):
      s3_client_instance.upload(mock_file_name)

    s3_client_instance.boto_client.upload_file.assert_called_once_with(
        mock_file_name,
        s3_client_instance.bucket_name,
        os.path.basename(mock_file_name),
    )
