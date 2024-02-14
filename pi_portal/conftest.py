"""Global test fixtures."""

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.configuration.tests.fixtures import mock_state


@pytest.fixture
def test_state(monkeypatch: pytest.MonkeyPatch) -> state.State:
  """Create the default test state."""
  instance = state.State()

  monkeypatch.setattr(
      instance,
      "user_config",
      mock_state.mock_user_state_creator(),
  )
  monkeypatch.setattr(
      instance,
      "log_uuid",
      mock_state.MOCK_LOG_UUID,
  )
  monkeypatch.setattr(
      instance,
      "log_level",
      mock_state.MOCK_LOG_LEVEL,
  )

  return instance
