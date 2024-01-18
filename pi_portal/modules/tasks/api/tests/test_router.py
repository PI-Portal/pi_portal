"""Test the RouteFactory class."""

from unittest import mock

from fastapi import APIRouter
from .. import router


class TestRouteFactory:
  """Test the RouteFactory class."""

  def test_initialize__attributes(
      self,
      router_factory_instance: router.RouterFactory,
      mocked_scheduler: mock.Mock,
  ) -> None:
    assert isinstance(
        router_factory_instance.router,
        APIRouter,
    )
    assert router_factory_instance.scheduler == mocked_scheduler

  def test_create__returns_router(
      self,
      router_factory_instance: router.RouterFactory,
  ) -> None:
    instance = router_factory_instance.create()

    assert isinstance(instance, APIRouter)

  def test_create__schedule_task__has_a_created_route(
      self,
      router_factory_instance: router.RouterFactory,
  ) -> None:
    instance = router_factory_instance.create()

    instance.url_path_for("schedule_task")
