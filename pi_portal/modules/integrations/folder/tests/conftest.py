"""Test fixtures for the folder module's tests."""
# pylint: disable=redefined-outer-name

from dataclasses import dataclass
from typing import Dict

import pytest
from pi_portal.modules.integrations.folder import queue

MockedDirectoryType = Dict[str, "MockAttr"]


@pytest.fixture
def mocked_path() -> str:
  return "/var/path"


@dataclass
class MockAttr:
  m_time: int
  is_file: bool


@pytest.fixture
def disk_queue_instance(mocked_path: str) -> queue.DiskQueueIterator:
  return queue.DiskQueueIterator(mocked_path)


@pytest.fixture
def mocked_directory_contents() -> MockedDirectoryType:
  return {
      "sub_folder": MockAttr(1, False),
      "2.txt": MockAttr(1, True),
      "1.txt": MockAttr(0, True),
      "3.txt": MockAttr(4, True),
      "4.txt": MockAttr(5, True),
  }
