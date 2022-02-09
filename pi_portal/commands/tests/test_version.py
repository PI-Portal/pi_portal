"""Test the VersionCommand class."""

from unittest import mock

import pkg_resources
from pi_portal.commands.bases.tests.fixtures import command_harness
from .. import version


class TestVersionCommand(command_harness.CommandBaseTestHarness):
  """Test the VersionCommand class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = version.VersionCommand

  @mock.patch(version.__name__ + ".click")
  def test_invoke(self, m_module: mock.Mock) -> None:
    self.instance.invoke()
    m_module.echo.assert_called_once_with(
        f"Pi Portal Version: "
        f"{pkg_resources.get_distribution('pi_portal').version}",
    )
