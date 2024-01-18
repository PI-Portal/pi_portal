"""Task scheduler api server lifespan management."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from .security import SocketSecurity


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
  """FastAPI lifespan context."""
  socket_security = SocketSecurity()

  executor = ThreadPoolExecutor()
  executor.submit(app.state.scheduler.start)
  executor.submit(socket_security.rewrite_permissions)
  executor.shutdown(wait=False)

  yield
  app.state.scheduler.halt()
