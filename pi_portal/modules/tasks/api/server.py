"""The task scheduler API server."""

from typing import TYPE_CHECKING

from fastapi import FastAPI
from pi_portal.modules.tasks.api.lifespan import lifespan
from pi_portal.modules.tasks.api.router import RouterFactory

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.scheduler import TaskScheduler


class Server:
  """The task scheduler API server."""

  def __init__(self, scheduler: "TaskScheduler") -> None:
    """:param scheduler: The scheduler instance to provide an API for."""

    router_factory = RouterFactory(scheduler)
    self.api = FastAPI(
        docs_url=None,
        lifespan=lifespan,
        redoc_url=None,
    )
    self.api.state.scheduler = scheduler
    self.router = router_factory.create()
    self.api.include_router(self.router)
