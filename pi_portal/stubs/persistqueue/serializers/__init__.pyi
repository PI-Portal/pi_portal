"""Stubs for the persistqueue.serializers package."""

from typing import Any, BinaryIO, Protocol

# isort: off


class SerializerType(Protocol):
  dump: DumpType
  dumps: DumpsType
  load: LoadType
  loads: LoadsType


class DumpType(Protocol):

  def __call__(self, value: Any, fp: BinaryIO, sort_keys: bool = False) -> None:
    ...


class DumpsType(Protocol):

  def __call__(self, value: Any, sort_keys: bool = False) -> bytes:
    ...


class LoadType(Protocol):

  def __call__(self, fp: BinaryIO) -> Any:
    ...


class LoadsType(Protocol):

  def __call__(self, bytes_value: Any) -> Any:
    ...
