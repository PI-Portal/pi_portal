"""Test RunningConfig monostate."""

from unittest import TestCase, mock

from pi_portal.modules.configuration import state


class TestRunningConfig(TestCase):
  """Test the RunningConfig monostate."""

  def setUp(self) -> None:
    self.state = state.State()

  def test_mono_state(self) -> None:
    self.state.user_config = {
        'test': 'value'
    }

    instance2 = state.State()
    self.assertEqual(self.state.user_config, getattr(instance2, 'user_config'))

  @mock.patch(state.__name__ + ".UserConfiguration")
  def test_load_config(self, m_user_config: mock.Mock) -> None:
    mock_config = {
        "a": "b"
    }
    m_user_config.return_value.user_config = mock_config

    self.state.load()

    m_user_config.return_value.load.assert_called_once_with()
    self.assertEqual(self.state.user_config, mock_config)

    instance2 = state.State()
    self.assertEqual(self.state.user_config, instance2.user_config)
