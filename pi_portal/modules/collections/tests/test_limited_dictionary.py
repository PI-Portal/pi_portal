"""Test the LimitedDictionary class."""

from ..limited_dictionary import LimitedDictionary


class TestLimitedDictionary:
  """Test the LimitedDictionary class."""

  def test_initialize__no_default__attributes(self) -> None:
    limited_dictionary: \
        LimitedDictionary[str, int] = LimitedDictionary(10)

    assert limited_dictionary.limit == 10
    # pylint: disable=protected-access
    assert not limited_dictionary._internal

  def test_initialize__with_default_sequence__attributes(self) -> None:
    limited_dictionary: \
        LimitedDictionary[str, int] = LimitedDictionary(10, [("one", 1)])

    assert limited_dictionary.limit == 10
    # pylint: disable=protected-access
    assert limited_dictionary._internal == {"one": 1}

  def test_initialize__with_default_kwargs__attributes(self) -> None:
    limited_dictionary: \
      LimitedDictionary[str, int] = LimitedDictionary(10, one=1)

    assert limited_dictionary.limit == 10
    # pylint: disable=protected-access
    assert limited_dictionary._internal == {"one": 1}

  def test_initialize__with_default_dictionary__attributes(self) -> None:
    limited_dictionary: \
        LimitedDictionary[str, int] = LimitedDictionary(10, **{"one": 1})

    assert limited_dictionary.limit == 10
    # pylint: disable=protected-access
    assert limited_dictionary._internal == {"one": 1}

  def test_initialize__with_default_over_size_dictionary__attributes(
      self
  ) -> None:
    limited_dictionary: LimitedDictionary[str, int] = (
        LimitedDictionary(3, **{
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4
        })
    )

    assert limited_dictionary.limit == 3
    # pylint: disable=protected-access
    assert limited_dictionary._internal == {'two': 2, 'three': 3, 'four': 4}

  def test_contains__present__returns_true(
      self,
      limited_dictionary_multiple: LimitedDictionary[str, int],
  ) -> None:
    assert "one" in limited_dictionary_multiple

  def test_contains__not_present__returns_true(
      self,
      limited_dictionary_empty: LimitedDictionary[str, int],
  ) -> None:
    assert "one" not in limited_dictionary_empty

  def test_iter__multiple_values__keys(
      self,
      limited_dictionary_multiple: LimitedDictionary[str, int],
  ) -> None:
    assert list(limited_dictionary_multiple) == ["one", "two", "three"]

  def test_iter__multiple_values__items(
      self,
      limited_dictionary_multiple: LimitedDictionary[str, int],
  ) -> None:
    assert list(limited_dictionary_multiple.items()) == [
        ("one", 1), ("two", 2), ("three", 3)
    ]

  def test_len__multiple_values__returns_correct_length(
      self,
      limited_dictionary_multiple: LimitedDictionary[str, int],
  ) -> None:
    assert len(limited_dictionary_multiple) == 3

  def test_get_item__multiple_values__returns_correct_values(
      self,
      limited_dictionary_multiple: LimitedDictionary[str, int],
  ) -> None:
    assert limited_dictionary_multiple["one"] == 1
    assert limited_dictionary_multiple["two"] == 2
    assert limited_dictionary_multiple["three"] == 3

  def test_del_item__multiple_values__removes_key(
      self,
      limited_dictionary_multiple: LimitedDictionary[str, int],
  ) -> None:
    del limited_dictionary_multiple["one"]
    del limited_dictionary_multiple["two"]
    del limited_dictionary_multiple["three"]

    assert len(limited_dictionary_multiple) == 0

  def test_set_item__empty_dictionary__creates_key_value_pair(
      self,
      limited_dictionary_empty: LimitedDictionary[str, int],
  ) -> None:
    limited_dictionary_empty["ten"] = 10

    assert len(limited_dictionary_empty) == 1
    assert limited_dictionary_empty["ten"] == 10

  def test_set_item__full_dictionary__creates_key_value_pair(
      self,
      limited_dictionary_full: LimitedDictionary[str, int],
  ) -> None:
    values = list(limited_dictionary_full.items())

    limited_dictionary_full["twenty"] = 20

    assert len(limited_dictionary_full) == 10
    assert len(values) == 10
    assert list(limited_dictionary_full.items()) == \
        values[1:] + [("twenty", 20)]
