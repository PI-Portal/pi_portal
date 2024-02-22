"""Test the UnixStreamHttpClient class."""

import pytest
from ..unix_stream_http_client import (
    UnixStreamHttpClient,
    UnixStreamHttpClientException,
)
from .conftest import MockedResponse


class TestUnixStreamHttpClient:
  """Test the UnixStreamHttpClient class."""

  def test_initialize__attributes(
      self,
      mocked_socket_path: str,
      unix_stream_http_client_instance: UnixStreamHttpClient,
  ) -> None:
    assert unix_stream_http_client_instance.socket_path == mocked_socket_path

  def test_post__200__json_response__returns_json_response(
      self,
      mocked_response: MockedResponse,
      unix_stream_http_client_instance: UnixStreamHttpClient,
  ) -> None:
    mocked_response.write(b'{"result": "successful"}')
    mocked_response.reason = "OK"
    mocked_response.seek(0)
    mocked_response.status = 200

    response = unix_stream_http_client_instance.post(
        "/mock/path",
        {"mock": "body"},
    )

    assert response.status == 200
    assert response.json == {"result": "successful"}

  def test_post__200__non_json__returns_reason_response(
      self,
      mocked_response: MockedResponse,
      unix_stream_http_client_instance: UnixStreamHttpClient,
  ) -> None:
    mocked_response.write(b'Invalid JSON')
    mocked_response.reason = "OK"
    mocked_response.seek(0)
    mocked_response.status = 200

    response = unix_stream_http_client_instance.post(
        "/mock/path",
        {"mock": "body"},
    )

    assert response.status == 200
    assert response.json == {"detail": mocked_response.reason}

  def test_post__400__json_response__raises_exception(
      self,
      mocked_response: MockedResponse,
      unix_stream_http_client_instance: UnixStreamHttpClient,
  ) -> None:
    mocked_response.write(b'{"result": "failure"}')
    mocked_response.reason = "Not Found"
    mocked_response.seek(0)
    mocked_response.status = 400

    with pytest.raises(UnixStreamHttpClientException) as exc:
      unix_stream_http_client_instance.post(
          "/mock/path",
          {"mock": "body"},
      )

    assert exc.value.args == ({"result": "failure"},)

  def test_post__400__non_json_response__raises_exception(
      self,
      mocked_response: MockedResponse,
      unix_stream_http_client_instance: UnixStreamHttpClient,
  ) -> None:
    mocked_response.write(b'Invalid JSON')
    mocked_response.reason = "Not Found"
    mocked_response.seek(0)
    mocked_response.status = 400

    with pytest.raises(UnixStreamHttpClientException) as exc:
      unix_stream_http_client_instance.post(
          "/mock/path",
          {"mock": "body"},
      )

    assert exc.value.args == ({"detail": mocked_response.reason},)
