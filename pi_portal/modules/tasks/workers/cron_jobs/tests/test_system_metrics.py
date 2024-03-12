"""Test the system_metrics module."""

from io import StringIO

import pytest
from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from .. import system_metrics
from ..bases import cron_job_base
from ..mixins import metrics_logger
from .conftest import SystemMetricsScenario, TypeSystemMetricsScenarioCreator


@pytest.mark.usefixtures("test_state")
class TestSystemMetricsCronJob:
  """Test the system_metrics module."""

  def test_initialize__attributes(
      self,
      system_metrics_cron_job_instance: system_metrics.CronJob,
  ) -> None:
    assert system_metrics_cron_job_instance.interval == \
        config.CRON_INTERVAL_SYSTEM_METRICS
    assert system_metrics_cron_job_instance.name == "System Metrics"
    assert system_metrics_cron_job_instance.quiet is True
    assert system_metrics_cron_job_instance.type == \
        enums.TaskType.NON_SCHEDULED

  def test_initialize__inheritance(
      self,
      system_metrics_cron_job_instance: system_metrics.CronJob,
  ) -> None:
    assert isinstance(
        system_metrics_cron_job_instance,
        metrics_logger.MetricsLoggerMixin,
    )
    assert isinstance(
        system_metrics_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__returns_correct_value(
      self,
      system_metrics_cron_job_instance: system_metrics.CronJob,
  ) -> None:
    expected_args = non_scheduled.Args()

    # pylint: disable=protected-access
    assert system_metrics_cron_job_instance._args() == expected_args

  @pytest.mark.parametrize(
      "scenario", [
          SystemMetricsScenario(
              disk_usage_free_mb=200,
              cpu_used_percent=20.5,
              virtual_memory_used_percent=5.7,
          ),
          SystemMetricsScenario(
              disk_usage_free_mb=1000,
              cpu_used_percent=10.1,
              virtual_memory_used_percent=60.0,
          )
      ]
  )
  def test_hook_submit__standard_logging(
      self,
      create_system_metrics_scenario: TypeSystemMetricsScenarioCreator,
      mocked_stream: StringIO,
      scenario: SystemMetricsScenario,
  ) -> None:
    scenario_mocks = create_system_metrics_scenario(scenario)

    scenario_mocks.system_metrics_cron_job_instance.schedule(
        scenario_mocks.mocked_task_scheduler
    )

    assert mocked_stream.getvalue() == ""

  @pytest.mark.parametrize(
      "scenario", [
          SystemMetricsScenario(
              disk_usage_free_mb=200,
              cpu_used_percent=20.5,
              virtual_memory_used_percent=5.7,
          ),
          SystemMetricsScenario(
              disk_usage_free_mb=1000,
              cpu_used_percent=10.1,
              virtual_memory_used_percent=60.0,
          )
      ]
  )
  def test_hook_submit__metrics_logging(
      self,
      create_system_metrics_scenario: TypeSystemMetricsScenarioCreator,
      mocked_metrics_stream: StringIO,
      test_state: state.State,
      scenario: SystemMetricsScenario,
  ) -> None:
    scenario_mocks = create_system_metrics_scenario(scenario)
    threshold = (
        test_state.user_config["CAMERA"]["DISK_SPACE_MONITOR"]["THRESHOLD"]
    )

    scenario_mocks.system_metrics_cron_job_instance.schedule(
        scenario_mocks.mocked_task_scheduler
    )

    assert mocked_metrics_stream.getvalue() == (
        "INFO - None - System Metrics - "
        "None - None - "
        "None - None - "
        "{'camera_disk_space_utilization': " +
        str(round(
            threshold / scenario.disk_usage_free_mb,
            2,
        ) * 100) + ", "
        "'cpu_utilization': " + str(scenario.cpu_used_percent) + ", "
        "'memory_utilization': " + str(scenario.virtual_memory_used_percent) +
        "} - " + "Raspberry Pi system metrics.\n"
    )
