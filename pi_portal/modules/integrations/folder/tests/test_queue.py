"""Test the DiskQueueIterator class."""

import os
from contextlib import contextmanager
from typing import Generator
from unittest import mock

from pi_portal.modules.integrations.folder import queue
from .conftest import MockedDirectoryType

QUEUE_MODULE = queue.__name__


class TestDiskQueueIterator:
  """Test the DiskQueueIterator class."""

  test_path = "/var/path"

  @staticmethod
  @contextmanager
  def mocked_filesystem_context(
      mocked_filesystem_content: MockedDirectoryType
  ) -> Generator[None, None, None]:

    with mock.patch(QUEUE_MODULE + ".os.listdir") as m_listdir:
      with mock.patch(QUEUE_MODULE + ".os.path.isfile") as m_isfile:
        with mock.patch(QUEUE_MODULE + ".os.path.getmtime") as m_getmtime:
          try:
            m_listdir_return_value = []
            m_isfile_side_effects = []
            m_getmtime_side_effects = []

            for entry, attr in mocked_filesystem_content.items():
              m_listdir_return_value.append(entry)
              m_isfile_side_effects.append(attr.is_file)
              if attr.is_file:
                m_getmtime_side_effects.append(attr.m_time)

            m_listdir.return_value = m_listdir_return_value
            m_isfile.side_effect = m_isfile_side_effects
            m_getmtime.side_effect = m_getmtime_side_effects
            yield
          finally:
            pass

  def test__initialization__attrs(
      self,
      disk_queue_instance: queue.DiskQueueIterator,
      mocked_path: str,
  ) -> None:
    assert disk_queue_instance.path == mocked_path

  def test__interation__first_file(
      self,
      disk_queue_instance: queue.DiskQueueIterator,
      mocked_directory_contents: MockedDirectoryType,
  ) -> None:
    with self.mocked_filesystem_context(mocked_directory_contents):
      first_file = list(disk_queue_instance)

    assert first_file == [os.path.join(self.test_path, "1.txt")]

  def test__interation__folders_not_processed(
      self,
      disk_queue_instance: queue.DiskQueueIterator,
      mocked_directory_contents: MockedDirectoryType,
  ) -> None:
    for file_entry in list(mocked_directory_contents.keys()):
      if mocked_directory_contents[file_entry].is_file:
        del mocked_directory_contents[file_entry]

    with self.mocked_filesystem_context(mocked_directory_contents):
      next_filename = list(disk_queue_instance)

    assert not next_filename

  def test__interation__processing_order(
      self,
      disk_queue_instance: queue.DiskQueueIterator,
      mocked_directory_contents: MockedDirectoryType,
  ) -> None:
    processing_order = []

    while len(mocked_directory_contents) > 1:
      with self.mocked_filesystem_context(mocked_directory_contents):
        for next_filename in disk_queue_instance:
          del mocked_directory_contents[os.path.basename(next_filename)]
          processing_order.append(next_filename)

    assert processing_order == [
        os.path.join(self.test_path, f"{index}.txt") for index in range(1, 5)
    ]
