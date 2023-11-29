"""Global test fixtures."""

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.configuration.tests.fixtures import mock_state


@pytest.fixture
@mock_state.patch
def mocked_state() -> state.State:
  """Return the default mocked state."""
  return state.State()
