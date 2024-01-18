"""A metaclass that adds a _post_init__ method to initialization."""

import abc
from typing import Any, Dict, cast


class MetaPostInitCaller(type):
  """Metaclass that calls __post_init__ after being initialized."""

  def __call__(
      cls,
      *args: Any,
      **kwargs: Dict[str, Any],
  ) -> "MetaPostInitCaller":
    instance = type.__call__(cls, *args, **kwargs)
    instance.__post_init__()
    return cast(MetaPostInitCaller, instance)

  def __post_init__(cls) -> None:
    """Perform post initialization tasks."""


class MetaAbstractPostInitCaller(abc.ABCMeta, MetaPostInitCaller):
  """Abstract MetaPostInitCaller metaclass."""
