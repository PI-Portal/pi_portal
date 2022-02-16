"""Fixtures for mocking required environment variables."""
import logging
from typing import Any, Callable, TypeVar
from unittest import mock

from pi_portal.modules.configuration import state

MOCK_AWS_ACCESS_KEY_ID = "awsKeyId"
MOCK_AWS_SECRET_ACCESS_KEY = "awsKeySecret"
MOCK_LOGZ_IO_CODE = "secretCode"
MOCK_SLACK_CHANNEL = "mockChannel"
MOCK_SLACK_CHANNEL_ID = "CHHH111"
MOCK_SLACK_TOKEN = "secretValue"
MOCK_S3_BUCKET_NAME = 'MOCK_S3_BUCKET_NAME'
MOCK_LOG_UUID = "MOCK_UUID_VALUE"
MOCK_LOG_LEVEL = logging.DEBUG

TypeReturn = TypeVar("TypeReturn")


def patch(func: Callable[..., TypeReturn]) -> Callable[..., TypeReturn]:

  def patched_function(*args: Any, **kwargs: Any) -> TypeReturn:

    with mock.patch(state.__name__ + ".State") as mock_state:

      mock_state_instance = mock_state.return_value
      mock_state_instance.user_config = {
          "AWS_ACCESS_KEY_ID": MOCK_AWS_ACCESS_KEY_ID,
          "AWS_SECRET_ACCESS_KEY": MOCK_AWS_SECRET_ACCESS_KEY,
          "LOGZ_IO_CODE": MOCK_LOGZ_IO_CODE,
          "SLACK_BOT_TOKEN": MOCK_SLACK_TOKEN,
          "SLACK_CHANNEL": MOCK_SLACK_CHANNEL,
          "SLACK_CHANNEL_ID": MOCK_SLACK_CHANNEL_ID,
          "S3_BUCKET_NAME": MOCK_S3_BUCKET_NAME,
          "CONTACT_SWITCHES": [{
              "NAME": "Front",
              "GPIO": 5,
          }],
          "DHT11_SENSORS": [{
              "NAME": "Kitchen",
              "GPIO": 4,
          }]
      }
      mock_state_instance.log_uuid = MOCK_LOG_UUID
      mock_state_instance.log_level = MOCK_LOG_LEVEL

      return func(*args, **kwargs)

  return patched_function
