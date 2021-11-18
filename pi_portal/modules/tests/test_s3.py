"""Test S3 Integration."""

from unittest import TestCase, mock

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from pi_portal.modules import s3
from pi_portal.modules.tests.fixtures import mock_state


class TestS3Bucket(TestCase):
  """Test the S3Bucket class."""

  @mock_state.patch
  @mock.patch(s3.__name__ + ".boto3")
  def setUp(self, m_boto):  # pylint: disable=arguments-differ
    self.s3_client = s3.S3Bucket()
    self.s3_client.boto_client = m_boto.return_value

  @mock_state.patch
  def test_initialization(self):
    s3_client = s3.S3Bucket()
    self.assertEqual(s3_client.bucket_name, mock_state.MOCK_S3_BUCKET_NAME)
    self.assertIsInstance(s3_client.boto_client, BaseClient)

  @mock_state.patch
  @mock.patch(s3.__name__ + ".boto3")
  def test_boto_client_initialization(self, m_boto):
    s3.S3Bucket()
    m_boto.client.assert_called_once_with(
        's3',
        aws_access_key_id=mock_state.MOCK_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=mock_state.MOCK_AWS_SECRET_ACCESS_KEY,
    )

  def test_upload_file(self):
    mock_file_name = "mock_file_name.mp4"
    self.s3_client.upload(mock_file_name)
    self.s3_client.boto_client.upload_file.assert_called_once_with(
        mock_file_name, self.s3_client.bucket_name, mock_file_name
    )

  def test_upload_file_exception(self):
    self.s3_client.boto_client.upload_file.side_effect = ClientError(
        error_response={}, operation_name="BOOM!"
    )
    mock_file_name = "mock_file_name.mp4"

    with self.assertRaises(s3.S3BucketException):
      self.s3_client.upload(mock_file_name)

    self.s3_client.boto_client.upload_file.assert_called_once_with(
        mock_file_name, self.s3_client.bucket_name, mock_file_name
    )
