"""Global test fixtures."""

import logging
from typing import List

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.configuration.tests.fixtures import mock_state


class OptionalFieldsLoggingFilter(logging.Filter):
  """Enable optional fields in test logging."""

  optional_fields: List[str]

  def filter(self, record: logging.LogRecord) -> bool:
    for field_name in self.optional_fields:
      if not hasattr(record, field_name):
        setattr(record, field_name, None)
    return True


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
