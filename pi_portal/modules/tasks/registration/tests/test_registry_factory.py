"""Test the RegistryFactory class."""
from unittest import mock

from .. import registry_factory


class TestRegistryFactory:
  """Test the RegistryFactory class."""

  def test_initialize__attributes__task_modules(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
  ) -> None:
    assert task_registry_factory_instance.task_modules == [
        # pylint: disable=duplicate-code
        "archive_logs",
        "archive_videos",
        "chat_send_message",
        "chat_upload_snapshot",
        "chat_upload_video",
        "file_system_move",
        "file_system_remove",
        "motion_snapshot",
        "non_scheduled",
        "queue_maintenance",
    ]

  def test_initialize__attributes__cron_modules(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
  ) -> None:
    assert task_registry_factory_instance.cron_job_modules == [
        # pylint: disable=duplicate-code
        "archive_logs",
        "archive_videos",
        "dead_man_switch",
        "queue_maintenance",
        "queue_metrics",
    ]

  def test_create__once__returns_registry(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
      mocked_task_registry: mock.Mock,
  ) -> None:
    return_value = task_registry_factory_instance.create()

    assert return_value == mocked_task_registry.return_value

  def test_create__twice__returns_same_registry(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
      task_registry_factory_instance_clone: registry_factory.RegistryFactory,
  ) -> None:
    return_value1 = task_registry_factory_instance.create()
    return_value2 = task_registry_factory_instance_clone.create()

    assert return_value1 == return_value2

  def test_create__once__initializes_registry(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
      mocked_task_registry: mock.Mock,
  ) -> None:
    task_registry_factory_instance.create()

    mocked_task_registry.assert_called_once_with()

  def test_create__twice__initializes_registry_once(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
      task_registry_factory_instance_clone: registry_factory.RegistryFactory,
      mocked_task_registry: mock.Mock,
  ) -> None:
    task_registry_factory_instance.create()
    task_registry_factory_instance_clone.create()

    mocked_task_registry.assert_called_once_with()

  def test_create__once__registers_correct_tasks(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
      mocked_task_registry: mock.Mock,
  ) -> None:
    mocked_register_task = mocked_task_registry.return_value.register_task

    task_registry_factory_instance.create()

    assert mocked_register_task.mock_calls == list(
        map(mock.call, task_registry_factory_instance.task_modules)
    )

  def test_create__twice__registers_correct_tasks_once(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
      task_registry_factory_instance_clone: registry_factory.RegistryFactory,
      mocked_task_registry: mock.Mock,
  ) -> None:
    mocked_register_task = mocked_task_registry.return_value.register_task

    task_registry_factory_instance.create()
    task_registry_factory_instance_clone.create()

    assert mocked_register_task.mock_calls == list(
        map(mock.call, task_registry_factory_instance.task_modules)
    )

  def test_create__once__registers_correct_cron_jobs(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
      mocked_task_registry: mock.Mock,
  ) -> None:
    mocked_register_cron_job = \
        mocked_task_registry.return_value.register_cron_job

    task_registry_factory_instance.create()

    assert mocked_register_cron_job.mock_calls == list(
        map(mock.call, task_registry_factory_instance.cron_job_modules)
    )

  def test_create__twice__registers_correct_cron_jobs_once(
      self,
      task_registry_factory_instance: registry_factory.RegistryFactory,
      task_registry_factory_instance_clone: registry_factory.RegistryFactory,
      mocked_task_registry: mock.Mock,
  ) -> None:
    mocked_register_cron_job = \
        mocked_task_registry.return_value.register_cron_job

    task_registry_factory_instance.create()
    task_registry_factory_instance_clone.create()

    assert mocked_register_cron_job.mock_calls == list(
        map(mock.call, task_registry_factory_instance.cron_job_modules)
    )
