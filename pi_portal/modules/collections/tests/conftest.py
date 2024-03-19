"""Test fixtures for the limited utility module tests."""

import pytest
from ..limited_dictionary import LimitedDictionary


@pytest.fixture
def limited_dictionary_empty() -> LimitedDictionary[str, int]:
  return LimitedDictionary(10)


@pytest.fixture
def limited_dictionary_multiple() -> LimitedDictionary[str, int]:
  return LimitedDictionary(10, one=1, two=2, three=3)


@pytest.fixture
def limited_dictionary_full() -> LimitedDictionary[str, int]:
  return LimitedDictionary(
      10, **{
          "one": 1,
          "two": 2,
          "three": 3,
          "four": 4,
          "five": 5,
          "six": 6,
          "seven": 7,
          "eight": 8,
          "nine": 9,
          "ten": 10
      }
  )
