"""Configuration for the task scheduler service."""

from typing import Dict

from .enums import TaskPriority

QUEUE_WORKER_CONFIGURATION: Dict[TaskPriority, int] = {
    TaskPriority.STANDARD: 4,
    TaskPriority.EXPRESS: 2
}
