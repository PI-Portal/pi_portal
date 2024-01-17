"""Test fixtures for the network modules tests."""
# pylint: disable=redefined-outer-name,duplicate-code

import logging
from contextlib import closing
from io import BytesIO, StringIO
from typing import TYPE_CHECKING, TextIO
from unittest import mock

import pytest
from .. import http

if TYPE_CHECKING:
  StreamHandlerType = logging.StreamHandler[TextIO]  # pragma: no cover
else:
  StreamHandlerType = logging.StreamHandler


@pytest.fixture
def mocked_file_handle_binary() -> BytesIO:
  return BytesIO()


@pytest.fixture
def mocked_logger(mocked_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test")
  handler = logging.StreamHandler(stream=mocked_stream)
  handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  return logger


@pytest.fixture
def mocked_open_write_binary(mocked_file_handle_binary: BytesIO) -> mock.Mock:
  open_mock = mock.Mock()
  open_mock.return_value = closing(mocked_file_handle_binary)

  return open_mock


@pytest.fixture
def mocked_requests_adapter() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_requests_session() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def http_client_instance(
    mocked_logger: logging.Logger,
    mocked_open_write_binary: mock.Mock,
    mocked_shutil: mock.Mock,
    mocked_requests_adapter: mock.Mock,
    mocked_requests_session: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> http.HttpClient:
  monkeypatch.setattr(
      "builtins.open",
      mocked_open_write_binary,
  )
  monkeypatch.setattr(
      http.__name__ + ".shutil",
      mocked_shutil,
  )
  monkeypatch.setattr(
      http.__name__ + ".HTTPAdapter",
      mocked_requests_adapter,
  )
  monkeypatch.setattr(
      http.__name__ + ".Session",
      mocked_requests_session,
  )
  return http.HttpClient(mocked_logger)
