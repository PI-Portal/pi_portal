"""Test the compatibility shim."""

import sys
from types import ModuleType
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
    with self.assertRaises(shim.IncompatiblePlatform) as exc:
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


class TestImportOrMock(TestCase):
  """Test the import_or_mock function."""

  def setUp(self) -> None:
    self.mock_modules = mock.MagicMock()
    self.mock_modules.__setitem__.side_effect = ModuleNotFoundError("Boom!")
    self.reset_module("adafruit_dht")
    self.reset_module("board")

  def tearDown(self) -> None:
    self.reset_module("adafruit_dht")
    self.reset_module("board")

  def reset_module(self, name: str) -> None:
    if name in sys.modules:
      del sys.modules[name]

  @mock.patch(shim.__name__ + ".os.uname", MOCK_X86)
  def test_import_or_mock_x86(self) -> None:
    self.assertIsInstance(
        shim.import_or_mock("adafruit_dht"),
        mock.MagicMock,
    )

  @mock.patch(shim.__name__ + ".os.uname", MOCK_ARM)
  def test_import_or_mock_arm(self) -> None:
    self.assertIsInstance(shim.import_or_mock("adafruit_dht"), ModuleType)

  @mock.patch(shim.__name__ + ".os.uname", MOCK_ARM)
  @mock.patch(
      shim.__name__ + ".import_module",
      mock.Mock(side_effect=NotImplementedError)
  )
  def test_import_or_mock_arm_exception(self) -> None:
    self.assertIsInstance(
        shim.import_or_mock("board"),
        mock.MagicMock,
    )

  @mock.patch(shim.__name__ + ".os.uname", MOCK_ARM)
  @mock.patch(
      shim.__name__ + ".import_module",
      mock.Mock(side_effect=NotImplementedError)
  )
  def test_import_or_mock_arm_exception_dual_import(self) -> None:
    first_import = shim.import_or_mock("board")
    second_import = shim.import_or_mock("board")

    self.assertEqual(
        first_import,
        second_import,
    )
