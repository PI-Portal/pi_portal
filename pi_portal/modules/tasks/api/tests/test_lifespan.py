"""Test the FastAPI lifespan context manager."""

from unittest import mock

from fastapi.testclient import TestClient


class TestApi:
  """Test the FastAPI lifespan context manager."""

  def test_lifespan__two_threads_are_launched(
      self,
      test_client_threads: TestClient,
      mocked_scheduler: mock.Mock,
      mocked_socket_security: mock.Mock,
      mocked_threadpool_executor: mock.Mock,
  ) -> None:
    with test_client_threads:

      mocked_threadpool_executor.assert_called_once_with()
      assert mocked_threadpool_executor.return_value.submit.mock_calls == [
          mock.call(mocked_scheduler.start),
          mock.call(mocked_socket_security.return_value.rewrite_permissions),
      ]
      mocked_threadpool_executor.return_value.shutdown.\
          assert_called_once_with(wait=False)

  def test_lifespan__scheduler_is_started(
      self,
      test_client_threads: TestClient,
      mocked_scheduler: mock.Mock,
  ) -> None:
    with test_client_threads:

      assert mocked_scheduler.start.is_called_once_with()

  def test_lifespan__scheduler_is_halted(
      self,
      test_client_threads: TestClient,
      mocked_scheduler: mock.Mock,
  ) -> None:
    with test_client_threads:
      pass

    mocked_scheduler.halt.assert_called_once_with()

  def test_lifespan__socket_security_is_called(
      self,
      test_client_threads: TestClient,
      mocked_socket_security: mock.Mock,
  ) -> None:
    with test_client_threads:

      mocked_socket_security.assert_called_once_with()
      mocked_socket_security.return_value.\
          rewrite_permissions.asset_called_once_with()
