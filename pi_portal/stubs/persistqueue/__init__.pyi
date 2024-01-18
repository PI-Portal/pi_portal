"""Stubs for the persistqueue package."""

from typing import Any, Optional, Tuple, Union

import persistqueue.serializers.pickle
from .serializers import SerializerType

# isort: off


class SQLiteAckQueue(SQLiteBase):

  def __init__(
      self,
      path: str,
      auto_resume: bool = True,
      name: str = 'default',
      multithreading: bool = False,
      timeout: float = 10.0,
      auto_commit: bool = True,
      serializer: SerializerType = persistqueue.serializers.pickle,
      db_file_name: Optional[str] = None,
  ) -> None:
    ...

  def ack(
      self,
      item: Optional[Any] = None,
      id: Optional[int] = None,
  ) -> Optional[int]:
    ...

  def acked_count(self) -> int:
    ...

  def clear_acked_data(
      self,
      max_delete: int = 1000,
      keep_latest: int = 1000,
      clear_ack_failed: bool = False
  ) -> Tuple[str, str]:
    ...

  def put(self, item: Any) -> int:
    ...

  def nack(
      self,
      item: Optional[Any] = None,
      id: Optional[int] = None,
  ) -> Optional[int]:
    ...

  def unack_count(self) -> int:
    ...


class SQLiteBase:

  def __init__(
      self,
      path: str,
      name: str = 'default',
      multithreading: bool = False,
      timeout: float = 10.0,
      auto_commit: bool = True,
      serializer: SerializerType = persistqueue.serializers.pickle,
      db_file_name: Optional[str] = None,
  ) -> None:
    ...

  def get(
      self,
      block: bool = True,
      timeout: Optional[int] = None,
      id: Optional[int] = None,
      raw: bool = False,
  ) -> Union[dict[str, Any], dict[str, Any], None]:
    ...

  def shrink_disk_usage(self) -> Tuple[str, Tuple[()]]:
    ...

  @property
  def size(self) -> int:
    ...
