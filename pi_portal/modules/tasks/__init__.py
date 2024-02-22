"""Pi Portal task modules."""

from importlib import import_module
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:  # pragma: no cover
  from fastapi import FastAPI


def create_service() -> "FastAPI":
  """Entrypoint for bootstrapping the tasks service."""
  service_module = import_module("pi_portal.modules.tasks.service")
  task_scheduler_service = service_module.TaskSchedulerService()
  return cast("FastAPI", task_scheduler_service.server.api)
