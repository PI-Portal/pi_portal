"""Pi Portal task modules."""

from typing import TYPE_CHECKING

from pi_portal.modules.tasks.service import TaskSchedulerService

if TYPE_CHECKING:  # pragma: no cover
  from fastapi import FastAPI


def create_service() -> "FastAPI":  # pragma: no cover
  """Entrypoint for bootstrapping the tasks service."""

  task_scheduler_service = TaskSchedulerService()
  return task_scheduler_service.server.api
