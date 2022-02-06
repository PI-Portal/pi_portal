"""Test the compatibility shim."""

from unittest import TestCase, mock

from .. import shim

MOCK_ARM = mock.Mock(return_value=(None, None, None, None, "arm"))
MOCK_X86 = mock.Mock(return_value=(None, None, None, None, "x86"))


class TestPatchGPIO(TestCase):
  """Test the patch_gpio function."""

  def setUp(self) -> None:
    self.mock_modules = mock.MagicMock()
    self.mock_modules.__setitem__.side_effect = ModuleNotFoundError("Boom!")

  @mock.patch(shim.__name__ + ".sys")
  @mock.patch(shim.__name__ + ".os.uname", MOCK_X86)
  def test_patch_gpio_x86(self, m_sys: mock.Mock) -> None:
    m_sys.modules = self.mock_modules
    with self.assertRaises(Exception) as exc:
      shim.patch_gpio()
    self.assertEqual(
        exc.exception.args,
        ("This application is designed to be run on a Raspberry Pi.",),
    )

  @mock.patch(shim.__name__ + ".sys")
  @mock.patch(shim.__name__ + ".os.uname", MOCK_ARM)
  def test_patch_gpio_arm(self, m_sys: mock.Mock) -> None:
    m_sys.modules = self.mock_modules
    shim.patch_gpio()
