"""Test RunningConfig monostate."""

from unittest import TestCase, mock

from pi_portal.modules import state


class TestRunningConfig(TestCase):
  """Test the RunningConfig monostate."""

  def setUp(self):
    self.state = state.State()

  def test_mono_state(self):
    self.state.test_attribute = 100

    instance2 = state.State()
    self.assertEqual(
        self.state.test_attribute, getattr(instance2, 'test_attribute')
    )

  @mock.patch(state.__name__ + ".config_file.UserConfiguration")
  def test_load_config(self, m_user_config):
    mock_config = {
        "a": "b"
    }
    m_user_config.return_value.load.return_value = mock_config

    self.state.load()
    self.assertEqual(self.state.user_config, mock_config)

    instance2 = state.State()
    self.assertEqual(self.state.user_config, instance2.user_config)
