"""Test the S3BucketClient class."""

import os
from unittest import mock

import pytest
from botocore.exceptions import ClientError
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.archival.aws import client
from pi_portal.modules.integrations.archival.bases.client import (
    ArchivalClientBase,
    ArchivalException,
)


@pytest.mark.usefixtures("test_state")
class TestS3BucketClient:
  """Test the S3BucketClient class."""

  def test_initialization__attributes(
      self,
      aws_archival_client_instance: client.S3BucketClient,
      mocked_bucket_name: str,
  ) -> None:
    assert aws_archival_client_instance.partition_name == mocked_bucket_name

  def test_initialization__boto_client(
      self,
      aws_archival_client_instance: client.S3BucketClient,
      mocked_boto: mock.Mock,
      test_state: state.State,
  ) -> None:
    aws_config = test_state.user_config["ARCHIVAL"]["AWS"]
    assert aws_archival_client_instance.boto_client == (
        mocked_boto.client.return_value
    )
    mocked_boto.client.assert_called_once_with(
        's3',
        aws_access_key_id=aws_config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=aws_config['AWS_SECRET_ACCESS_KEY'],
    )

  def test_initialization__inheritance(
      self,
      aws_archival_client_instance: client.S3BucketClient,
  ) -> None:
    assert isinstance(
        aws_archival_client_instance,
        client.S3BucketClient,
    )
    assert isinstance(
        aws_archival_client_instance,
        ArchivalClientBase,
    )

  def test_upload__success(
      self,
      aws_archival_client_instance: client.S3BucketClient,
  ) -> None:
    mock_file_name = "/dir/mock_file_name.mp4"
    mock_object_name = os.path.basename(mock_file_name)

    aws_archival_client_instance.upload(mock_file_name, mock_object_name)

    aws_archival_client_instance.boto_client.\
        upload_file.assert_called_once_with(
            mock_file_name,
            aws_archival_client_instance.partition_name,
            mock_object_name,
        )

  def test__upload__exception(
      self,
      aws_archival_client_instance: client.S3BucketClient,
  ) -> None:
    aws_archival_client_instance.boto_client.upload_file.side_effect = (
        ClientError(
            error_response={},
            operation_name="BOOM!",
        )
    )
    mock_file_name = "/dir/mock_file_name.mp4"
    mock_object_name = os.path.basename(mock_file_name)

    with pytest.raises(ArchivalException):
      aws_archival_client_instance.upload(mock_file_name, mock_object_name)

    aws_archival_client_instance.boto_client.\
        upload_file.assert_called_once_with(
            mock_file_name,
            aws_archival_client_instance.partition_name,
            mock_object_name,
        )
