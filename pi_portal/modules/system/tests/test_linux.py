"""Test Linux Utilities."""

from unittest import TestCase, mock

from pi_portal.modules.system import linux


class TestLinux(TestCase):
  """Test the Linux utilities module."""

  mock_uptime = 52675.05
  mock_uptime_as_string = "14 hours"

  @mock.patch(linux.__name__ + ".time.monotonic")
  def test_uptime(self, m_mono: mock.Mock) -> None:
    m_mono.return_value = self.mock_uptime
    result = linux.uptime()
    self.assertEqual(result, self.mock_uptime_as_string)
    m_mono.assert_called_once_with()
