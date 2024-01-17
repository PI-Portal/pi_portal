"""Test the HttpClient Class."""
import logging
from io import BytesIO, StringIO
from unittest import mock

import pytest
import urllib3
from .. import http


class TestHttpClient:
  """Test the HttpClient Class."""

  mock_remote_url = "https://mock.url/mock_file_content"
  mock_local_target = "/mock_path/mock_file.txt"

  def test_initialize__attributes(
      self,
      http_client_instance: http.HttpClient,
  ) -> None:
    assert isinstance(
        http_client_instance.log,
        logging.Logger,
    )
    assert http_client_instance.basic_auth is None

  def test_initialize__retry_config(
      self,
      http_client_instance: http.HttpClient,
  ) -> None:
    assert isinstance(
        http_client_instance.retry_config,
        urllib3.Retry,
    )
    assert http_client_instance.retry_config.redirect == 5
    assert http_client_instance.retry_config.total == 5

  def test__set_basic_auth__is_stored(
      self,
      http_client_instance: http.HttpClient,
  ) -> None:
    http_client_instance.set_basic_auth("username1", "password1")

    assert http_client_instance.basic_auth == ("username1", "password1")

  def test__get__with_target__success__logging(
      self,
      http_client_instance: http.HttpClient,
      mocked_stream: StringIO,
  ) -> None:
    http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    assert mocked_stream.getvalue() == (
        f"INFO - HTTP GET: '{self.mock_remote_url}' ...\n"
        f"INFO - HTTP GET: Connected to '{self.mock_remote_url}' ...\n"
        f"INFO - HTTP GET: Successfully saved "
        f"'{self.mock_local_target}' !\n"
    )

  def test__get__without_target__success__logging(
      self,
      http_client_instance: http.HttpClient,
      mocked_stream: StringIO,
  ) -> None:
    http_client_instance.get(self.mock_remote_url)

    assert mocked_stream.getvalue() == (
        f"INFO - HTTP GET: '{self.mock_remote_url}' ...\n"
        f"INFO - HTTP GET: Connected to '{self.mock_remote_url}' ...\n"
    )

  def test__get__with_target__success__adapter(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_adapter: mock.Mock,
  ) -> None:
    http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    mocked_requests_adapter.assert_called_once_with(
        max_retries=http_client_instance.retry_config
    )

  def test__get__without_target__success__adapter(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_adapter: mock.Mock,
  ) -> None:
    http_client_instance.get(self.mock_remote_url)

    mocked_requests_adapter.assert_called_once_with(
        max_retries=http_client_instance.retry_config
    )

  def test__get__with_target__no_auth__success__session(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_adapter: mock.Mock,
      mocked_requests_session: mock.Mock,
  ) -> None:
    http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    assert mocked_requests_session.mock_calls == [
        mock.call(),
        mock.call().mount("http://", mocked_requests_adapter.return_value),
        mock.call().mount("https://", mocked_requests_adapter.return_value),
        mock.call().get(self.mock_remote_url, stream=True),
    ]

  def test__get__with_target__with_auth__success__session(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_adapter: mock.Mock,
      mocked_requests_session: mock.Mock,
  ) -> None:
    http_client_instance.set_basic_auth("username", "password")

    http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    assert mocked_requests_session.mock_calls == [
        mock.call(),
        mock.call().mount("http://", mocked_requests_adapter.return_value),
        mock.call().mount("https://", mocked_requests_adapter.return_value),
        mock.call().get(self.mock_remote_url, stream=True),
    ]
    assert mocked_requests_session.return_value.auth == \
        http_client_instance.basic_auth

  def test__get__without_target__no_auth__success__session(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_adapter: mock.Mock,
      mocked_requests_session: mock.Mock,
  ) -> None:
    http_client_instance.get(self.mock_remote_url)

    assert mocked_requests_session.mock_calls == [
        mock.call(),
        mock.call().mount("http://", mocked_requests_adapter.return_value),
        mock.call().mount("https://", mocked_requests_adapter.return_value),
        mock.call().get(self.mock_remote_url, stream=True),
    ]

  def test__get__without_target__with_auth__success__session(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_adapter: mock.Mock,
      mocked_requests_session: mock.Mock,
  ) -> None:
    http_client_instance.set_basic_auth("username", "password")

    http_client_instance.get(self.mock_remote_url)

    assert mocked_requests_session.mock_calls == [
        mock.call(),
        mock.call().mount("http://", mocked_requests_adapter.return_value),
        mock.call().mount("https://", mocked_requests_adapter.return_value),
        mock.call().get(self.mock_remote_url, stream=True),
    ]
    assert mocked_requests_session.return_value.auth == \
        http_client_instance.basic_auth

  def test__get__with_target__success__open(
      self,
      http_client_instance: http.HttpClient,
      mocked_open_write_binary: mock.Mock,
  ) -> None:
    http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    mocked_open_write_binary.assert_called_once_with(
        self.mock_local_target,
        "wb",
    )

  def test__get__without_target__success__open(
      self,
      http_client_instance: http.HttpClient,
      mocked_open_write_binary: mock.Mock,
      mocked_requests_session: mock.Mock,
  ) -> None:
    response = http_client_instance.get(self.mock_remote_url)

    mocked_open_write_binary.assert_not_called()
    assert response == mocked_requests_session.return_value.get.return_value

  def test__get__with_target__success__copyfileobj(
      self,
      http_client_instance: http.HttpClient,
      mocked_file_handle_binary: BytesIO,
      mocked_requests_session: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    mocked_shutil.copyfileobj.assert_called_once_with(
        mocked_requests_session.return_value.get.return_value.raw,
        mocked_file_handle_binary,
    )

  def test__get__without_target__success__copyfileobj(
      self,
      http_client_instance: http.HttpClient,
      mocked_shutil: mock.Mock,
  ) -> None:
    http_client_instance.get(self.mock_remote_url)

    mocked_shutil.copyfileobj.assert_not_called()

  def test__get__with_target__failure__logging(
      self,
      http_client_instance: http.HttpClient,
      mocked_stream: StringIO,
      mocked_requests_session: mock.Mock,
  ) -> None:
    mocked_requests_session.return_value.get.return_value.ok = False

    with pytest.raises(http.HttpClientError) as exc:
      http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    assert mocked_stream.getvalue() == (
        f"INFO - HTTP GET: '{self.mock_remote_url}' ...\n"
        "ERROR - HTTP GET: Unable to retrieve remote file from "
        f"'{self.mock_remote_url}' !\n"
    )
    assert str(exc.value) == \
        self.mock_remote_url

  def test__get__with_target__failure__adapter(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_adapter: mock.Mock,
      mocked_requests_session: mock.Mock,
  ) -> None:
    mocked_requests_session.return_value.get.return_value.ok = False

    with pytest.raises(http.HttpClientError):
      http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    mocked_requests_adapter.assert_called_once_with(
        max_retries=http_client_instance.retry_config
    )

  def test__get__with_target__failure__session(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_adapter: mock.Mock,
      mocked_requests_session: mock.Mock,
  ) -> None:
    mocked_requests_session.return_value.get.return_value.ok = False

    with pytest.raises(http.HttpClientError):
      http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    assert mocked_requests_session.mock_calls == [
        mock.call(),
        mock.call().mount("http://", mocked_requests_adapter.return_value),
        mock.call().mount("https://", mocked_requests_adapter.return_value),
        mock.call().get(self.mock_remote_url, stream=True),
    ]

  def test__get__with_target__failure__open(
      self,
      http_client_instance: http.HttpClient,
      mocked_open_write_binary: mock.Mock,
      mocked_requests_session: mock.Mock,
  ) -> None:
    mocked_requests_session.return_value.get.return_value.ok = False

    with pytest.raises(http.HttpClientError):
      http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    mocked_open_write_binary.assert_not_called()

  def test__get__with_target__failure__copyfileobj(
      self,
      http_client_instance: http.HttpClient,
      mocked_requests_session: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    mocked_requests_session.return_value.get.return_value.ok = False

    with pytest.raises(http.HttpClientError):
      http_client_instance.get(self.mock_remote_url, self.mock_local_target)

    mocked_shutil.copyfileobj.assert_not_called()
