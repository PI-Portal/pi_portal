"""Task scheduler worker base class."""
import abc


class WorkerBase(abc.ABC):
  """Abstract task scheduler worker class."""

  @abc.abstractmethod
  def start(self) -> None:
    """Start the worker."""

  @abc.abstractmethod
  def halt(self) -> None:
    """Stop the worker."""
