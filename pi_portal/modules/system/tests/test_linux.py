"""Test Linux Utilities."""

from unittest import mock

from pi_portal.modules.system import linux


class TestLinux:
  """Test the Linux utilities module."""

  mock_uptime = 52675.05
  mock_uptime_as_string = "14 hours"

  @mock.patch(linux.__name__ + ".time.monotonic")
  def test_uptime__correct_value(
      self,
      m_monotonic: mock.Mock,
  ) -> None:
    m_monotonic.return_value = self.mock_uptime

    result = linux.uptime()

    assert result == self.mock_uptime_as_string
    m_monotonic.assert_called_once_with()
