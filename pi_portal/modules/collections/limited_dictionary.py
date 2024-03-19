"""LimitedDictionary class."""

from typing import (
    Any,
    Dict,
    Generic,
    Iterator,
    MutableMapping,
    Sequence,
    Tuple,
    TypeVar,
    cast,
)

K = TypeVar('K')
V = TypeVar('V')


class LimitedDictionary(Generic[K, V], MutableMapping[K, V]):
  """A size bounded dictionary."""

  def __init__(
      self,
      limit: int,
      *initial_values: Sequence[Tuple[K, V]],
      **initial_dictionary: V,
  ):
    self.limit = limit
    self._internal: Dict[K, V] = dict(
        *initial_values,
        **cast(Dict[K, V], initial_dictionary),
    )
    while len(self) > limit:
      self.popitem()

  def __contains__(self, key: Any) -> bool:
    return key in self._internal

  def __iter__(self) -> Iterator[K]:
    return iter(self._internal)

  def __len__(self) -> int:
    return len(self._internal)

  def __getitem__(self, key: K) -> V:
    return self._internal[key]

  def __delitem__(self, key: K) -> None:
    del self._internal[key]

  def __setitem__(self, key: K, value: V) -> None:
    if key not in self and len(self) == self.limit:
      self.popitem()
    self._internal[key] = value
