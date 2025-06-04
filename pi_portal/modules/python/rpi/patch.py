"""Raspberry PI GPIO compatibility shim."""

import importlib
import os
import sys
from typing import Optional
from unittest import mock


def patch_module(
    module_name: str,
    substitute_module: Optional[str] = None,
) -> None:
  """Mock or substitute an import if not running on the 'arm' platform.

  If substitute_module is None, the module will be mocked.
  Otherwise, the module will be replaced.

  :param module_name: The module to import.
  :param substitute_module: An optional module to substitute for the import.
  """

  if os.getenv("PI_PORTAL_MOCK_GPIO", None):
    sys.modules[module_name] = mock.Mock()
    return

  if not (os.uname()[4].startswith("arm") or os.uname()[4].startswith("aarch")):
    if not substitute_module:
      sys.modules[module_name] = mock.Mock()
    else:
      sys.modules[module_name] = importlib.import_module(substitute_module)
