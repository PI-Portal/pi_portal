"""Fixtures for mocking required environment variables."""

import logging
from contextlib import contextmanager
from typing import Any, Callable, Generator, TypeVar
from unittest import mock

from pi_portal.modules.configuration import state

MOCK_AWS_ACCESS_KEY_ID = "awsKeyId"
MOCK_AWS_SECRET_ACCESS_KEY = "awsKeySecret"
MOCK_AWS_S3_BUCKETS = {
    'LOGS': 'MOCK_S3_BUCKET_NAME_1',
    'VIDEOS': 'MOCK_S3_BUCKET_NAME_2',
}
MOCK_LOGZ_IO_CODE = "secretCode"
MOCK_SLACK_CHANNEL = "mockChannel"
MOCK_SLACK_CHANNEL_ID = "CHHH111"
MOCK_SLACK_APP_SIGNING_SECRET = "MOCK_SLACK_APP_SIGNING_SECRET"
MOCK_SLACK_APP_TOKEN = "MOCK_SLACK_APP_TOKEN"
MOCK_SLACK_BOT_TOKEN = "secretValue"
MOCK_LOG_UUID = "MOCK_UUID_VALUE"
MOCK_LOG_LEVEL = logging.DEBUG

TypeReturn = TypeVar("TypeReturn")


def patch(func: Callable[..., TypeReturn]) -> Callable[..., TypeReturn]:

  def patched_function(*args: Any, **kwargs: Any) -> TypeReturn:

    with mock_state_creator():
      return func(*args, **kwargs)

  return patched_function


@contextmanager
def mock_state_creator() -> Generator[mock.Mock, None, None]:
  with mock.patch(state.__name__ + ".State") as mock_state:
    try:
      mock_state_instance = mock_state.return_value
      mock_state_instance.user_config = {
          "AWS_ACCESS_KEY_ID": MOCK_AWS_ACCESS_KEY_ID,
          "AWS_SECRET_ACCESS_KEY": MOCK_AWS_SECRET_ACCESS_KEY,
          "AWS_S3_BUCKETS": MOCK_AWS_S3_BUCKETS,
          "LOGZ_IO_CODE": MOCK_LOGZ_IO_CODE,
          "SLACK_APP_SIGNING_SECRET": MOCK_SLACK_APP_SIGNING_SECRET,
          "SLACK_APP_TOKEN": MOCK_SLACK_APP_TOKEN,
          "SLACK_BOT_TOKEN": MOCK_SLACK_BOT_TOKEN,
          "SLACK_CHANNEL": MOCK_SLACK_CHANNEL,
          "SLACK_CHANNEL_ID": MOCK_SLACK_CHANNEL_ID,
          "CONTACT_SWITCHES": [{
              "NAME": "Front",
              "GPIO": 5,
          }],
          "TEMPERATURE_SENSORS": {
              "DHT11": [{
                  "NAME": "Kitchen",
                  "GPIO": 4,
              }]
          }
      }
      mock_state_instance.log_uuid = MOCK_LOG_UUID
      mock_state_instance.log_level = MOCK_LOG_LEVEL
      yield mock_state_instance
    finally:
      pass
