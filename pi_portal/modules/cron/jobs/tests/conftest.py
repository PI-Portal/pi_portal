"""Test fixtures for the cron job tests."""

import logging

import pytest
from pi_portal.modules.configuration.tests.fixtures import mock_state
from .. import dead_man_switch, video_upload


@pytest.fixture
def dead_man_switch_cron_job_instance(
    mocked_cron_logger: logging.Logger
) -> dead_man_switch.DeadManSwitchCronJob:
  return dead_man_switch.DeadManSwitchCronJob(mocked_cron_logger)


@pytest.fixture
def video_upload_cron_job_instance(
    mocked_cron_logger: logging.Logger
) -> video_upload.VideoUploadCronJob:
  with mock_state.mock_state_creator():
    instance = video_upload.VideoUploadCronJob(mocked_cron_logger)
  return instance
