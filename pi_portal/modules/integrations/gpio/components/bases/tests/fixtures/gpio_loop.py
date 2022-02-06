"""Test helpers to control the GPIO monitoring loop."""

from functools import wraps
from typing import Any, Callable, TypeVar, cast
from unittest import mock

TypeTestCaseMethod = TypeVar('TypeTestCaseMethod', bound=Callable[..., None])


def patch_gpio_loop(
    class_path: str
) -> Callable[[TypeTestCaseMethod], TypeTestCaseMethod]:
  """Patch the monitor loop so it iterates only once.

  :param class_path: The dot path to the class being patched for testing.
  :returns: The test method being decorated.
  """

  def decorator(test_function: TypeTestCaseMethod) -> TypeTestCaseMethod:

    @wraps(test_function)
    def wrapper(*args: Any, **kwargs: Any) -> None:
      with mock.patch(
          class_path + ".is_running", mock.Mock(side_effect=[True, False])
      ):
        return test_function(*args, **kwargs)

    return cast(TypeTestCaseMethod, wrapper)

  return decorator
