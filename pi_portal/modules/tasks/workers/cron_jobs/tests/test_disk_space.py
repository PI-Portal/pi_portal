"""Test the disk_space module."""

from io import StringIO
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.camera.service_client import CameraClient
from pi_portal.modules.system import supervisor_config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.non_scheduled import Args as DiskSpaceArgs
from .. import disk_space
from ..bases import cron_job_base
from .conftest import DiskSpaceScenario, TypeDiskSpaceScenarioCreator


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
    assert disk_space_cron_job_instance.type == \
        enums.TaskType.NON_SCHEDULED

  def test_initialize__camera_client(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
  ) -> None:
    assert isinstance(
        disk_space_cron_job_instance.camera_client,
        CameraClient,
    )

  def test_initialize__process(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    assert disk_space_cron_job_instance.process == (
        mocked_supervisor_process.return_value
    )
    mocked_supervisor_process.assert_called_once_with(
        supervisor_config.ProcessList.CAMERA
    )

  def test_initialize__task_scheduler_client(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
      mocked_task_scheduler_client: mock.Mock,
  ) -> None:
    assert disk_space_cron_job_instance.task_scheduler_client == (
        mocked_task_scheduler_client.return_value
    )
    mocked_task_scheduler_client.assert_called_once_with()

  def test_initialize__inheritance(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
  ) -> None:
    assert isinstance(
        disk_space_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__returns_correct_value(
      self,
      disk_space_cron_job_instance: disk_space.CronJob,
  ) -> None:
    expected_args = DiskSpaceArgs()

    # pylint: disable=protected-access
    assert disk_space_cron_job_instance._args() == expected_args

  @pytest.mark.parametrize(
      "disk_space_scenario", [
          DiskSpaceScenario(
              low_disk_space=True,
              camera_running=True,
          ),
          DiskSpaceScenario(
              low_disk_space=True,
              camera_running=False,
          )
      ]
  )
  def test_process__low_space__vary_camera__stops_process(
      self,
      create_disk_space_scenario: TypeDiskSpaceScenarioCreator,
      disk_space_scenario: DiskSpaceScenario,
  ) -> None:
    scenario = create_disk_space_scenario(disk_space_scenario)

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    scenario.mocked_supervisor_process.return_value.\
        stop.assert_called_once_with()

  @pytest.mark.parametrize(
      "disk_space_scenario",
      [DiskSpaceScenario(
          low_disk_space=True,
          camera_running=True,
      )]
  )
  def test_process__low_space__camera_on__sends_message(
      self,
      create_disk_space_scenario: TypeDiskSpaceScenarioCreator,
      disk_space_scenario: DiskSpaceScenario,
  ) -> None:
    scenario = create_disk_space_scenario(disk_space_scenario)

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    scenario.mocked_task_scheduler_client.return_value.\
        chat_send_message.assert_called_once_with(
          scenario.disk_space_cron_job_instance.low_disk_space_message
        )

  @pytest.mark.parametrize(
      "disk_space_scenario",
      [DiskSpaceScenario(
          low_disk_space=True,
          camera_running=True,
      )]
  )
  def test_process__low_space__camera_on__logging(
      self,
      create_disk_space_scenario: TypeDiskSpaceScenarioCreator,
      mocked_stream: StringIO,
      test_state: state.State,
      disk_space_scenario: DiskSpaceScenario,
  ) -> None:
    scenario = create_disk_space_scenario(disk_space_scenario)
    camera_config = test_state.user_config["CAMERA"]

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    assert mocked_stream.getvalue() == (
        f"WARNING - None - {scenario.disk_space_cron_job_instance.name} - "
        "None - Camera storage disk space is now below the "
        f"{camera_config['DISK_SPACE_MONITOR']['THRESHOLD']} MB(s) "
        f"threshold.\n"
        f"WARNING - None - {scenario.disk_space_cron_job_instance.name} - "
        "None - Camera has been deactivated due to lack of disk space.\n"
    )

  @pytest.mark.parametrize(
      "disk_space_scenario",
      [DiskSpaceScenario(
          low_disk_space=True,
          camera_running=False,
      )]
  )
  def test_process__low_space__camera_off__does_not_send_message(
      self,
      create_disk_space_scenario: TypeDiskSpaceScenarioCreator,
      disk_space_scenario: DiskSpaceScenario,
  ) -> None:
    scenario = create_disk_space_scenario(disk_space_scenario)

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    scenario.mocked_task_scheduler.router.put.assert_not_called()

  @pytest.mark.parametrize(
      "disk_space_scenario",
      [DiskSpaceScenario(
          low_disk_space=True,
          camera_running=False,
      )]
  )
  def test_process__low_space__camera_off__logging(
      self,
      create_disk_space_scenario: TypeDiskSpaceScenarioCreator,
      mocked_stream: StringIO,
      test_state: state.State,
      disk_space_scenario: DiskSpaceScenario,
  ) -> None:
    scenario = create_disk_space_scenario(disk_space_scenario)
    camera_config = test_state.user_config["CAMERA"]

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    assert mocked_stream.getvalue() == (
        f"WARNING - None - {scenario.disk_space_cron_job_instance.name} - "
        "None - Camera storage disk space is now below the "
        f"{camera_config['DISK_SPACE_MONITOR']['THRESHOLD']} MB(s) "
        f"threshold.\n"
    )

  @pytest.mark.parametrize(
      "disk_space_scenario", [
          DiskSpaceScenario(
              low_disk_space=False,
              camera_running=True,
          ),
          DiskSpaceScenario(
              low_disk_space=False,
              camera_running=False,
          ),
      ]
  )
  def test_process__ok_space__vary_camera__does_not_stop_process(
      self,
      create_disk_space_scenario: TypeDiskSpaceScenarioCreator,
      disk_space_scenario: DiskSpaceScenario,
  ) -> None:
    scenario = create_disk_space_scenario(disk_space_scenario)

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    scenario.mocked_supervisor_process.return_value.stop.assert_not_called()

  @pytest.mark.parametrize(
      "disk_space_scenario", [
          DiskSpaceScenario(
              low_disk_space=False,
              camera_running=True,
          ),
          DiskSpaceScenario(
              low_disk_space=False,
              camera_running=False,
          ),
      ]
  )
  def test_process__ok_space__vary_camera__does_not_send_message(
      self,
      create_disk_space_scenario: TypeDiskSpaceScenarioCreator,
      disk_space_scenario: DiskSpaceScenario,
  ) -> None:
    scenario = create_disk_space_scenario(disk_space_scenario)

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    scenario.mocked_task_scheduler.router.put.assert_not_called()

  @pytest.mark.parametrize(
      "disk_space_scenario", [
          DiskSpaceScenario(
              low_disk_space=False,
              camera_running=True,
          ),
          DiskSpaceScenario(
              low_disk_space=False,
              camera_running=False,
          ),
      ]
  )
  def test_process__ok_space__vary_camera__logging(
      self,
      create_disk_space_scenario: TypeDiskSpaceScenarioCreator,
      mocked_stream: StringIO,
      disk_space_scenario: DiskSpaceScenario,
  ) -> None:
    scenario = create_disk_space_scenario(disk_space_scenario)

    scenario.disk_space_cron_job_instance.schedule(
        scenario.mocked_task_scheduler
    )

    assert mocked_stream.getvalue() == ""
