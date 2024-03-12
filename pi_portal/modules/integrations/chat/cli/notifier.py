"""Notifier for the chat CLI."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.service_client import TaskSchedulerServiceClient


class ChatCLINotifier:
  """Notifier for the chat CLI.

  :param task_scheduler_client: The configured task scheduler client to use.
  """

  def __init__(
      self,
      task_scheduler_client: "TaskSchedulerServiceClient",
  ) -> None:
    self.task_scheduler_client = task_scheduler_client

  def notify_already_start(self) -> None:
    """Report that the service is already up."""

    self.task_scheduler_client.chat_send_message("Already running ...")

  def notify_already_stop(self) -> None:
    """Report that the service is already down."""

    self.task_scheduler_client.chat_send_message("Already stopped ...")

  def notify_error(self) -> None:
    """Report that an error has occurred."""

    self.task_scheduler_client.chat_send_message(
        "An internal error occurred ... you better take a look."
    )

  def notify_insufficient_disk_space(self) -> None:
    """Report that there is insufficient disk space available.."""

    self.task_scheduler_client.chat_send_message(
        "There is insufficient disk space to do that right now ..."
    )

  def notify_start(self) -> None:
    """Report that the service is starting."""

    self.task_scheduler_client.chat_send_message("Starting ...")

  def notify_stop(self) -> None:
    """Report that the service is stopping."""

    self.task_scheduler_client.chat_send_message("Shutting down ...")
