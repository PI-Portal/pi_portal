"""Task scheduler API router factory."""

from fastapi import APIRouter
from pi_portal.modules.tasks.scheduler import TaskScheduler
from pi_portal.modules.tasks.task.serializers.task_serializer import (
    SerializedTask,
)
from .model import TaskCreationRequestModel


class RouterFactory:
  """Create a populated FastAPI router from the task registry.

  :param scheduler: The scheduler instance the API is provided for.
  """

  def __init__(
      self,
      scheduler: TaskScheduler,
  ) -> None:
    self.router = APIRouter()
    self.scheduler = scheduler

  def create(self) -> APIRouter:
    """Create and populate a FastAPI router using the task registry.

    :returns: The populated router.
    """
    self._create_endpoint()

    return self.router

  def _create_endpoint(self) -> None:

    async def create_task(
        creation_request: TaskCreationRequestModel
    ) -> "SerializedTask":
      new_task = creation_request.as_task()
      self.scheduler.router.put(new_task)
      return SerializedTask.serialize(new_task)

    self.router.add_api_route(
        "/schedule/",
        create_task,
        name="schedule_task",
        response_model=None,
        methods=["POST"],
    )
