"""Test the Server class."""

from unittest import mock

from .. import lifespan, server


class TestServer:
  """Test the Server class."""

  def test_initialize__fast_api(
      self,
      server_instance_with_mocked_fast_api: server.Server,
      mocked_fast_api: mock.Mock,
      mocked_router_factory: mock.Mock,
      mocked_scheduler: mock.Mock,
  ) -> None:
    mocked_fast_api.assert_called_once_with(
        docs_url=None,
        lifespan=lifespan.lifespan,
        redoc_url=None,
    )
    assert server_instance_with_mocked_fast_api.api == \
        mocked_fast_api.return_value
    assert server_instance_with_mocked_fast_api.api.state.scheduler == \
        mocked_scheduler
    mocked_fast_api.return_value.include_router.assert_called_once_with(
        mocked_router_factory.return_value.create.return_value
    )

  def test_initialize__router_factory(
      self,
      server_instance_with_mocked_fast_api: server.Server,
      mocked_router_factory: mock.Mock,
      mocked_scheduler: mock.Mock,
  ) -> None:
    mocked_router_factory.assert_called_once_with(mocked_scheduler)
    mocked_router_factory.return_value.create.assert_called_once_with()
    assert server_instance_with_mocked_fast_api.router == \
           mocked_router_factory.return_value.create.return_value
