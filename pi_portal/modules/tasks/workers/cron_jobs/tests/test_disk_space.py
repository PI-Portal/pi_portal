"""Test the disk_space module."""

from io import StringIO
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.integrations.camera.service_client import CameraClient
from pi_portal.modules.system import supervisor_config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.config import DEFERRED_MESSAGE_PREFIX
from pi_portal.modules.tasks.task import (
    chat_send_message,
    flag_set_value,
    supervisor_process,
)
from .. import disk_space
from ..bases import cron_job_base


@pytest.mark.usefixtures("test_state")
class TestDiskSpaceCronJob:
  """Test the disk_space module."""

  def test_initialize__attributes(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
  ) -> None:
    assert disk_space_cron_job_instance.interval == \
        config.CRON_INTERVAL_DISK_SPACE
    assert disk_space_cron_job_instance.low_disk_space_message == (
        "Watch out!  We're running out of disk space!\n"
        "** The camera has been shut off! **"
    )
    assert disk_space_cron_job_instance.name == "Disk Space"
    assert disk_space_cron_job_instance.quiet is True
    assert disk_space_cron_job_instance.resume_camera_message == (
        "We now have enough disk space to run the camera!\n"
        "** The camera has been reactivated! **"
    )
    assert disk_space_cron_job_instance.type == \
        enums.TaskType.SUPERVISOR_PROCESS

  def test_initialize__camera_client(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
  ) -> None:
    assert isinstance(
        disk_space_cron_job_instance.camera_client,
        CameraClient,
    )

  def test_initialize__inheritance(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
  ) -> None:
    assert isinstance(
        disk_space_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__low_space__returns_correct_value(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
  ) -> None:
    disk_space_cron_job_instance.has_sufficient_disk_space = False
    expected_args = supervisor_process.Args(
        process=supervisor_config.ProcessList.CAMERA,
        requested_state=supervisor_config.ProcessStatus.STOPPED
    )

    # pylint: disable=protected-access
    assert disk_space_cron_job_instance._args() == expected_args

  def test_args__good_space__returns_correct_value(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
  ) -> None:
    disk_space_cron_job_instance.has_sufficient_disk_space = True
    expected_args = supervisor_process.Args(
        process=supervisor_config.ProcessList.CAMERA,
        requested_state=supervisor_config.ProcessStatus.RUNNING
    )

    # pylint: disable=protected-access
    assert disk_space_cron_job_instance._args() == expected_args

  def test_process__low_space__enabled_flag__logging(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = True
    mocked_is_disk_space_available.return_value = False

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    assert mocked_stream.getvalue() == ""

  def test_process__low_space__enabled_flag__does_not_schedule_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_is_disk_space_available.return_value = False
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = False

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    mocked_task_scheduler.router.assert_not_called()

  def test_process__low_space__disabled_flag__logging(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    camera_config = disk_space_cron_job_instance.camera_client.camera_config
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = False
    mocked_is_disk_space_available.return_value = False

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    assert mocked_stream.getvalue() == (
        "WARNING - None - None - "
        f"{disk_space_cron_job_instance.name} - "
        "None - Camera storage disk space is now below the "
        f"{camera_config['DISK_SPACE_MONITOR']['THRESHOLD']} MB(s) "
        f"threshold.\n"
    )

  def test_process__low_space__disabled_flag__schedules_correct_process_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_is_disk_space_available.return_value = False
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = False

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    task = mocked_task_scheduler.router.put.mock_calls[0].args[0]
    assert isinstance(task, supervisor_process.Task)
    assert task.args.process == supervisor_config.ProcessList.CAMERA
    assert task.args.requested_state == supervisor_config.ProcessStatus.STOPPED
    assert len(task.on_success) == 2

  def test_process__low_space__disabled_flag__schedules_correct_chat_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_is_disk_space_available.return_value = False
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = False

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    task = mocked_task_scheduler.router.put.mock_calls[0].args[0].on_success[0]
    assert isinstance(task, chat_send_message.Task)
    assert task.args.message == (
        disk_space_cron_job_instance.low_disk_space_message
    )

  def test_process__low_space__disabled_flag__schedules_correct_chat_retry_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_is_disk_space_available.return_value = False
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = False

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    task = mocked_task_scheduler.router.put.mock_calls[0].args[0].on_success[0]
    assert len(task.on_failure) == 1
    retry_task = task.on_failure[0]
    assert isinstance(retry_task, chat_send_message.Task)
    assert retry_task.args.message == (
        DEFERRED_MESSAGE_PREFIX +
        disk_space_cron_job_instance.low_disk_space_message
    )
    assert retry_task.retry_after == 300

  def test_process__low_space__disabled_flag__schedules_correct_flag_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_is_disk_space_available.return_value = False
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = False

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    task = mocked_task_scheduler.router.put.mock_calls[0].args[0].on_success[1]
    assert isinstance(task, flag_set_value.Task)
    assert task.args.flag_name == "FLAG_CAMERA_DISABLED_BY_CRON"
    assert task.args.value is True
    assert task.retry_after == 30

  def test_process__good_space__enabled_flag__logging(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    camera_config = disk_space_cron_job_instance.camera_client.camera_config
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = True
    mocked_is_disk_space_available.return_value = True

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    assert mocked_stream.getvalue() == (
        "INFO - None - None - "
        f"{disk_space_cron_job_instance.name} - "
        "None - Camera storage disk space is now above the "
        f"{camera_config['DISK_SPACE_MONITOR']['THRESHOLD']} MB(s) "
        f"threshold.\n"
    )

  def test_process__good_space__enabled_flag__schedules_correct_process_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = True
    mocked_is_disk_space_available.return_value = True

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    task = mocked_task_scheduler.router.put.mock_calls[0].args[0]
    assert isinstance(task, supervisor_process.Task)
    assert task.args.process == supervisor_config.ProcessList.CAMERA
    assert task.args.requested_state == supervisor_config.ProcessStatus.RUNNING
    assert len(task.on_success) == 2

  def test_process__good_space__enabled_flag__schedules_correct_chat_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = True
    mocked_is_disk_space_available.return_value = True

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    task = mocked_task_scheduler.router.put.mock_calls[0].args[0].on_success[0]
    assert isinstance(task, chat_send_message.Task)
    assert task.args.message == (
        disk_space_cron_job_instance.resume_camera_message
    )
    assert len(task.on_failure) == 1

  def test_process__good_space__enabled_flag__schedules_correct_chat_retry_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = True
    mocked_is_disk_space_available.return_value = True

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    task = mocked_task_scheduler.router.put.mock_calls[0].args[0].on_success[0]
    assert len(task.on_failure) == 1
    retry_task = task.on_failure[0]
    assert isinstance(retry_task, chat_send_message.Task)
    assert retry_task.args.message == (
        DEFERRED_MESSAGE_PREFIX +
        disk_space_cron_job_instance.resume_camera_message
    )
    assert retry_task.retry_after == 300

  def test_process__good_space__enabled_flag__schedules_correct_flag_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = True
    mocked_is_disk_space_available.return_value = True

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    task = mocked_task_scheduler.router.put.mock_calls[0].args[0].on_success[1]
    assert isinstance(task, flag_set_value.Task)
    assert task.args.flag_name == "FLAG_CAMERA_DISABLED_BY_CRON"
    assert task.args.value is False
    assert task.retry_after == 30

  def test_process__good_space__disabled_flag__logging(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = False
    mocked_is_disk_space_available.return_value = True

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    assert mocked_stream.getvalue() == ""

  def test_process__good_space__disabled_flag__does_not_schedule_task(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_flags: mock.Mock,
      mocked_is_disk_space_available: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_flags.FLAG_CAMERA_DISABLED_BY_CRON = False
    mocked_is_disk_space_available.return_value = True

    disk_space_cron_job_instance.schedule(mocked_task_scheduler)

    mocked_task_scheduler.router.put.assert_not_called()
