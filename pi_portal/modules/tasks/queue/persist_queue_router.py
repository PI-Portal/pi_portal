"""A persist-queue backed task router."""

import logging

from pi_portal.modules.tasks.enums import TaskPriority
from .bases.router_base import TaskRouterBase
from .persist_queue import Queue


class TaskRouter(TaskRouterBase):
  """A persist-queue back task router.

  :param log:  A logger instance.
  """

  def __init__(self, log: logging.Logger) -> None:
    self.queues = {}
    for priority in TaskPriority:
      self.queues[priority] = Queue(log, priority=priority)
