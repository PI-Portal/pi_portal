"""Test the ChatSendMessageProcessor class."""

import logging
from unittest import mock

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.chat_send_message import ProcessorClass
from pi_portal.modules.tasks.processor.mixins import chat_client


class TestChatSendMessageProcessor:
  """Test the ChatSendMessageProcessor class."""

  def test_initialize__attributes(
      self,
      chat_send_message_instance: ProcessorClass,
  ) -> None:
    assert chat_send_message_instance.type == \
        TaskType.CHAT_SEND_MESSAGE

  def test_initialize__logger(
      self,
      chat_send_message_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        chat_send_message_instance.log,
        logging.Logger,
    )
    assert chat_send_message_instance.log == mocked_task_logger

  def test_initialize__chat_client(
      self,
      chat_send_message_instance: ProcessorClass,
      mocked_chat_client: mock.Mock,
  ) -> None:
    assert chat_send_message_instance.client == \
        mocked_chat_client.return_value

  def test_initialize__inheritance(
      self,
      chat_send_message_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        chat_send_message_instance,
        processor_base.TaskProcessorBase,
    )
    assert isinstance(
        chat_send_message_instance,
        chat_client.ChatClientMixin,
    )

  def test_process__calls_send_message(
      self,
      chat_send_message_instance: ProcessorClass,
      mocked_chat_message_task: mock.Mock,
      mocked_chat_client: mock.Mock,
  ) -> None:
    chat_send_message_instance.process(mocked_chat_message_task)

    mocked_chat_client.return_value.send_message.assert_called_once_with(
        mocked_chat_message_task.args.message
    )
