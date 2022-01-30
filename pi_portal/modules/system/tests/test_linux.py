"""Test Linux Utilities."""

from unittest import TestCase, mock

from pi_portal.modules.system import linux

MOCK_UPTIME_CONTENT = "52675.05 102804.94"


class TestLinux(TestCase):
  """Test the Linux utilities module."""

  @mock.patch(
      linux.__name__ + ".open", mock.mock_open(read_data=MOCK_UPTIME_CONTENT)
  )
  def test_uptime(self):
    result = linux.uptime()
    self.assertEqual(result, '14 hours')
