"""Test the ActionBase class."""
import logging

from ..base_action import ActionBase


class TestActionBase:
  """Test the ActionBase class."""

  def test_initialize__attributes(
      self,
      concrete_action_base_instance: ActionBase,
  ) -> None:
    assert isinstance(concrete_action_base_instance.log, logging.Logger)

  def test_initialize__inheritance(
      self,
      concrete_action_base_instance: ActionBase,
  ) -> None:
    assert isinstance(
        concrete_action_base_instance,
        ActionBase,
    )
