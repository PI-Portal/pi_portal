"""Test helpers related to the GPIO monitoring loop."""

from functools import wraps
from typing import Any, Callable, TypeVar, cast
from unittest import mock

TypeMethod = TypeVar('TypeMethod', bound=Callable[..., None])


def patch_gpio_loop(class_path: str) -> Callable[[TypeMethod], TypeMethod]:
  """Patch the monitor loop so it iterates only once.

  :param class_path: The dot path to the class being patched for testing.
  :returns: The test method being decorated.
  """

  def decorator(test_function: TypeMethod) -> TypeMethod:

    @wraps(test_function)
    def wrapper(*args: Any, **kwargs: Any) -> None:
      with mock.patch(
          class_path + ".is_running", mock.Mock(side_effect=[True, False])
      ):
        return test_function(*args, **kwargs)

    return cast(TypeMethod, wrapper)

  return decorator
