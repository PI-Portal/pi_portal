"""Test user configuration loader."""

import os
from unittest import TestCase, mock

from pi_portal.modules import config_file

MOCK_CONFIG = '{"mock_setting": true}'


class TestLoad(TestCase):
  """Test the user configuration loader."""

  @mock.patch(
      config_file.__name__ + ".open", mock.mock_open(read_data=MOCK_CONFIG)
  )
  def test_load(self):
    result = config_file.load()
    self.assertEqual(result, {"mock_setting": True})

  @mock.patch.dict(os.environ, {"SPHINX": "1"}, clear=True)
  def test_load_sphinx(self):
    result = config_file.load()
    self.assertEqual(result, {})
