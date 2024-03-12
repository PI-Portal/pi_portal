"""System metrics for the Pi Portal project."""

import time
from datetime import timedelta

import humanize
import psutil


class SystemMetrics:
  """Report linux system metrics."""

  def cpu_usage(self) -> float:
    """Report the system's cpu utilization as a percentage.

    :returns: The percentage of the system's cpu that is used.
    """
    return psutil.cpu_percent(interval=1, percpu=False)

  def disk_usage(self, path: str) -> float:
    """Report the specified path's disk utilization as a percentage.

    :param path: The path to report the disk utilization for.
    :returns: The percentage of the path's disk that is used.
    """
    return psutil.disk_usage(path).percent

  def disk_usage_threshold(self, path: str, threshold: float) -> float:
    """Report the specified path's disk utilization as a percentage.

    :param path: The path to report the disk utilization for.
    :param threshold: The disk threshold (in MB) to report utilization of.
    :returns: The percentage of the path's disk that is used, with threshold.
    """
    disk_usage = psutil.disk_usage(path)
    threshold_disk_usage = round(
        disk_usage.used / (disk_usage.total - (threshold * 1000000)),
        2,
    ) * 100
    return threshold_disk_usage

  def memory_usage(self) -> float:
    """Report the system's memory utilization as a percentage.

    :returns: The percentage of the system's memory that is used.
    """
    return psutil.virtual_memory().percent

  def uptime(self) -> float:
    """Report the system's uptime.

    :returns: The system's uptime in seconds.
    """

    return time.monotonic()

  def uptime_naturalized(self) -> str:
    """Report the system's uptime.

    :returns: The system's uptime as a naturalized string.
    """

    uptime_timedelta = timedelta(seconds=self.uptime())
    return humanize.naturaldelta(uptime_timedelta)
