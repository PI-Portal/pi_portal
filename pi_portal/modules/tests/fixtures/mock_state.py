"""Fixtures for mocking required environment variables."""

from unittest import mock

from pi_portal.modules import state

MOCK_TOKEN = "secretValue"
MOCK_CHANNEL = "mockChannel"
MOCK_CHANNEL_ID = "CHHH111"
MOCK_S3_BUCKET_NAME = 'MOCK_S3_BUCKET_NAME'
MOCK_LOGZ_IO_CODE = "secretCode"


def patch(func):

  def patched_function(*args, **kwargs):

    with mock.patch(state.__name__ + ".State") as mock_state:

      mock_state.return_value.user_config = {
          "SLACK_BOT_TOKEN": MOCK_TOKEN,
          "SLACK_CHANNEL": MOCK_CHANNEL,
          "SLACK_CHANNEL_ID": MOCK_CHANNEL_ID,
          "S3_BUCKET_NAME": MOCK_S3_BUCKET_NAME,
          "LOGZ_IO_CODE": MOCK_LOGZ_IO_CODE
      }

      func(*args, **kwargs)

  return patched_function
