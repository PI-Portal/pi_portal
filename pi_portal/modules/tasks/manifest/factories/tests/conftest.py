"""Tests for the task manifest factories tests."""
# pylint: disable=redefined-outer-name

from typing import Type
from unittest import mock

import pytest
from .. import task_manifest_factory


@pytest.fixture
def mocked_vendor_class() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def task_manifest_factory_class(
    mocked_vendor_class: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[task_manifest_factory.TaskManifestFactory]:
  monkeypatch.setattr(
      task_manifest_factory.__name__ + ".TaskManifestFactory.vendor_class",
      mocked_vendor_class,
  )
  monkeypatch.setattr(
      task_manifest_factory.__name__ + ".TaskManifestFactory._manifests",
      {},
  )
  return task_manifest_factory.TaskManifestFactory
