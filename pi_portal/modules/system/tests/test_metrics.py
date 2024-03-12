"""Test the SystemMetrics class."""

from unittest import mock

import pytest
from pi_portal.modules.system import metrics


class TestSystemMetrics:
  """Test the SystemMetrics class."""

  def test_cpu_usage__calls_psutil(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_psutil: mock.Mock,
  ) -> None:
    metrics_instance.cpu_usage()

    mocked_psutil.cpu_percent.assert_called_once_with(interval=1, percpu=False)

  def test_cpu_usage__returns_expected_value(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_psutil: mock.Mock,
  ) -> None:
    result = metrics_instance.cpu_usage()

    assert result == mocked_psutil.cpu_percent.return_value

  def test_disk_usage__calls_psutil(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_file_path: str,
      mocked_psutil: mock.Mock,
  ) -> None:
    metrics_instance.disk_usage(mocked_file_path)

    mocked_psutil.disk_usage.assert_called_once_with(mocked_file_path)

  def test_disk_usage__returns_expected_value(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_file_path: str,
      mocked_psutil: mock.Mock,
  ) -> None:
    result = metrics_instance.disk_usage(mocked_file_path)

    assert result == mocked_psutil.disk_usage.return_value.percent

  @pytest.mark.parametrize("threshold", [500, 200, 100])
  def test_disk_usage_threshold__calls_psutil(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_file_path: str,
      mocked_psutil: mock.Mock,
      threshold: float,
  ) -> None:
    mocked_psutil.disk_usage.return_value.used = 400 * 1000000
    mocked_psutil.disk_usage.return_value.total = 1000 * 1000000
    metrics_instance.disk_usage_threshold(
        mocked_file_path,
        threshold,
    )

    mocked_psutil.disk_usage.assert_called_once_with(mocked_file_path)

  @pytest.mark.parametrize("threshold", [500, 200, 100])
  def test_disk_usage_threshold__returns_expected_value(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_file_path: str,
      mocked_psutil: mock.Mock,
      threshold: float,
  ) -> None:
    mocked_psutil.disk_usage.return_value.used = 400 * 1000000
    mocked_psutil.disk_usage.return_value.total = 1000 * 1000000
    result = metrics_instance.disk_usage_threshold(
        mocked_file_path,
        threshold,
    )

    assert result == round(
        mocked_psutil.disk_usage.return_value.used /
        (mocked_psutil.disk_usage.return_value.total - (threshold * 1000000)), 2
    ) * 100

  def test_memory_usage__calls_psutil(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_psutil: mock.Mock,
  ) -> None:
    metrics_instance.memory_usage()

    mocked_psutil.virtual_memory.assert_called_once_with()

  def test_memory_usage__returns_expected_value(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_psutil: mock.Mock,
  ) -> None:
    result = metrics_instance.memory_usage()

    assert result == mocked_psutil.virtual_memory.return_value.percent

  @pytest.mark.parametrize("uptime_seconds", [
      [52675.05],
      [5675.05],
  ])
  def test_uptime__returns_expected_value(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_monotonic: mock.Mock,
      uptime_seconds: float,
  ) -> None:
    mocked_monotonic.return_value = uptime_seconds

    result = metrics_instance.uptime()

    assert result == uptime_seconds

  @pytest.mark.parametrize(
      "uptime_seconds,naturalized", [
          [52675.05, "14 hours"],
          [5675.05, "an hour"],
      ]
  )
  def test_uptime_naturalized__returns_expected_value(
      self,
      metrics_instance: metrics.SystemMetrics,
      mocked_monotonic: mock.Mock,
      uptime_seconds: float,
      naturalized: str,
  ) -> None:
    mocked_monotonic.return_value = uptime_seconds

    result = metrics_instance.uptime_naturalized()

    assert result == naturalized
