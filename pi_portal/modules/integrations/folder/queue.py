"""DiskQueueIterator class."""

import os
from typing import List, Union


class DiskQueueIterator:
  """Use a disk folder as a processing queue.

  :param path: The disk path to use for processing.
  """

  path: str
  current: Union[str, None]

  def __init__(self, path: str) -> None:
    self.path = path
    self.current = None

  def __iter__(self) -> "DiskQueueIterator":
    return self

  def __next__(self) -> str:
    try:
      self.current = self._get_queue()[0]
      return self.current
    except IndexError:
      raise StopIteration  # pylint: disable=raise-missing-from

  def _get_queue(self) -> List[str]:
    all_entries = [
        os.path.join(self.path, file_name)
        for file_name in os.listdir(self.path)
    ]
    files_only = filter(os.path.isfile, all_entries)
    queue = sorted(files_only, key=os.path.getmtime)

    return queue
