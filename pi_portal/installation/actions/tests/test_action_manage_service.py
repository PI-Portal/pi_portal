"""Test the ManageServiceAction class."""

from io import StringIO
from typing import Dict
from unittest import mock

import pytest
from pi_portal.installation.services.bases.service_definition import (
    ServiceDefinition,
)
from ..action_manage_service import ManageServiceAction, ServiceOperation
from ..bases import base_action, base_system_call_action


class TestManageServiceAction:
  """Test the ManageServiceAction class."""

  def test_initialize__attributes(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
  ) -> None:
    assert isinstance(
        concrete_action_manage_service_instance.operation,
        ServiceOperation,
    )

  def test_initialize__service_definition(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
  ) -> None:
    assert concrete_action_manage_service_instance.service == (
        mocked_service_definition
    )
    assert isinstance(
        concrete_action_manage_service_instance.service, ServiceDefinition
    )

  def test_initialize__inheritance(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
  ) -> None:
    assert isinstance(
        concrete_action_manage_service_instance,
        base_action.ActionBase,
    )
    assert isinstance(
        concrete_action_manage_service_instance,
        base_system_call_action.SystemCallActionBase,
    )

  @pytest.mark.parametrize("operation", ServiceOperation)
  def test_invoke__vary_operation__calls_correct_method(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_manage_service_methods: Dict[str, mock.Mock],
      operation: ServiceOperation,
  ) -> None:
    concrete_action_manage_service_instance.operation = operation

    with mock.patch.multiple(
        concrete_action_manage_service_instance,
        **mocked_manage_service_methods,
    ):
      concrete_action_manage_service_instance.invoke()

    mocked_manage_service_methods[operation.value].\
        assert_called_once_with()

  def test_disable__system_v__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0]

    concrete_action_manage_service_instance.disable()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to disable the '{service}' service ...\n"
        "INFO - Executing: 'update-rc.d {system_v_service} disable' ...\n"
        "INFO - Service: done attempting to disable the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
    )

  def test_disable__system_v__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0]

    concrete_action_manage_service_instance.disable()

    system_v_service = mocked_service_definition.system_v_service_name
    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} disable"),
    ]

  def test_disable__systemd__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0]

    concrete_action_manage_service_instance.disable()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to disable the '{service}' service ...\n"
        "INFO - Executing: 'update-rc.d {system_v_service} disable' ...\n"
        "ERROR - Command: 'update-rc.d {system_v_service} disable' failed!\n"
        "WARNING - Service: unable to disable '{service}' via a System V "
        "service.\n"
        "INFO - Executing: 'systemctl disable {systemd_unit}' ...\n"
        "INFO - Service: done attempting to disable the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
        systemd_unit=mocked_service_definition.systemd_unit_name,
    )

  def test_disable__systemd__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0]

    concrete_action_manage_service_instance.disable()

    system_v_service = mocked_service_definition.system_v_service_name
    systemd_unit = mocked_service_definition.systemd_unit_name
    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} disable"),
        mock.call(f"systemctl disable {systemd_unit}")
    ]

  def test_disable__process_not_found__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 127]

    concrete_action_manage_service_instance.disable()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to disable the '{service}' service ...\n"
        "INFO - Executing: 'update-rc.d {system_v_service} disable' ...\n"
        "ERROR - Command: 'update-rc.d {system_v_service} disable' failed!\n"
        "WARNING - Service: unable to disable '{service}' via a System V "
        "service.\n"
        "INFO - Executing: 'systemctl disable {systemd_unit}' ...\n"
        "ERROR - Command: 'systemctl disable {systemd_unit}' failed!\n"
        "WARNING - Service: unable to disable '{service}' via systemd.\n"
        "WARNING - Service: The '{service}' service could not be disabled!\n"
        "WARNING - Service: This service should be controlled by pi_portal!  "
        "Please disable it manually if required!\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
        systemd_unit=mocked_service_definition.systemd_unit_name,
    )

  def test_disable__process_not_found__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 127]

    concrete_action_manage_service_instance.disable()

    system_v_service = mocked_service_definition.system_v_service_name
    systemd_unit = mocked_service_definition.systemd_unit_name
    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} disable"),
        mock.call(f"systemctl disable {systemd_unit}")
    ]

  def test_enable__system_v__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0]

    concrete_action_manage_service_instance.enable()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to enable the '{service}' service ...\n"
        "INFO - Executing: 'update-rc.d {system_v_service} enable' ...\n"
        "INFO - Service: done attempting to enable the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
    )

  def test_enable__system_v__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0]

    concrete_action_manage_service_instance.enable()

    system_v_service = mocked_service_definition.system_v_service_name
    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} enable"),
    ]

  def test_enable__systemd__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0, 0]

    concrete_action_manage_service_instance.enable()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to enable the '{service}' service ...\n"
        "INFO - Executing: 'update-rc.d {system_v_service} enable' ...\n"
        "ERROR - Command: 'update-rc.d {system_v_service} enable' failed!\n"
        "WARNING - Service: unable to enable '{service}' via a System V "
        "service.\n"
        "INFO - Executing: 'systemctl enable {systemd_unit}' ...\n"
        "INFO - Service: done attempting to enable the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
        systemd_unit=mocked_service_definition.systemd_unit_name,
    )

  def test_enable__systemd__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0]

    concrete_action_manage_service_instance.enable()

    system_v_service = mocked_service_definition.system_v_service_name
    systemd_unit = mocked_service_definition.systemd_unit_name
    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} enable"),
        mock.call(f"systemctl enable {systemd_unit}"),
    ]

  def test_enable__process_not_found__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 127]

    concrete_action_manage_service_instance.enable()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to enable the '{service}' service ...\n"
        "INFO - Executing: 'update-rc.d {system_v_service} enable' ...\n"
        "ERROR - Command: 'update-rc.d {system_v_service} enable' failed!\n"
        "WARNING - Service: unable to enable '{service}' via a System V "
        "service.\n"
        "INFO - Executing: 'systemctl enable {systemd_unit}' ...\n"
        "ERROR - Command: 'systemctl enable {systemd_unit}' failed!\n"
        "WARNING - Service: unable to enable '{service}' via systemd.\n"
        "ERROR - Service: IMPORTANT! The '{service}' service could not be "
        "enabled!\n"
        "ERROR - Service: Please enable and start it manually!\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
        systemd_unit=mocked_service_definition.systemd_unit_name,
    )

  def test_enable__process_not_found__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 127]

    concrete_action_manage_service_instance.enable()

    system_v_service = mocked_service_definition.system_v_service_name
    systemd_unit = mocked_service_definition.systemd_unit_name
    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} enable"),
        mock.call(f"systemctl enable {systemd_unit}"),
    ]

  def test_stop__system_v__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0]

    concrete_action_manage_service_instance.stop()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to stop the '{service}' service ...\n"
        "INFO - Executing: 'service {system_v_service} stop' ...\n"
        "INFO - Service: done attempting to stop the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
    )

  def test_stop__system_v__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0]

    concrete_action_manage_service_instance.stop()

    system_v_service = mocked_service_definition.system_v_service_name
    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} stop"),
    ]

  def test_stop__systemd__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0]

    concrete_action_manage_service_instance.stop()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to stop the '{service}' service ...\n"
        "INFO - Executing: 'service {system_v_service} stop' ...\n"
        "ERROR - Command: 'service {system_v_service} stop' failed!\n"
        "WARNING - Service: '{service}' is not running via a System V "
        "service.\n"
        "INFO - Executing: 'systemctl stop {systemd_unit}' ...\n"
        "INFO - Service: done attempting to stop the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
        systemd_unit=mocked_service_definition.systemd_unit_name,
    )

  def test_stop__systemd__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0]

    concrete_action_manage_service_instance.stop()

    system_v_service = mocked_service_definition.system_v_service_name
    systemd_unit = mocked_service_definition.systemd_unit_name
    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} stop"),
        mock.call(f"systemctl stop {systemd_unit}"),
    ]

  def test_stop__process_not_found__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 127]

    concrete_action_manage_service_instance.stop()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to stop the '{service}' service ...\n"
        "INFO - Executing: 'service {system_v_service} stop' ...\n"
        "ERROR - Command: 'service {system_v_service} stop' failed!\n"
        "WARNING - Service: '{service}' is not running via a System V "
        "service.\n"
        "INFO - Executing: 'systemctl stop {systemd_unit}' ...\n"
        "ERROR - Command: 'systemctl stop {systemd_unit}' failed!\n"
        "WARNING - Service: '{service}' is not running via a systemd unit.\n"
        "WARNING - Service: The '{service}' service does not appear to be "
        "running ...\n"
        "WARNING - Service: It could be running via an unknown init system.\n"
        "INFO - Service: done attempting to stop the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
        systemd_unit=mocked_service_definition.systemd_unit_name,
    )

  def test_stop__process_not_found__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 127]

    concrete_action_manage_service_instance.stop()

    system_v_service = mocked_service_definition.system_v_service_name
    systemd_unit = mocked_service_definition.systemd_unit_name
    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} stop"),
        mock.call(f"systemctl stop {systemd_unit}"),
    ]

  def test_start__system_v__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0]

    concrete_action_manage_service_instance.start()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to start the '{service}' service ...\n"
        "INFO - Executing: 'service {system_v_service} start' ...\n"
        "INFO - Service: done attempting to start the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
    )

  def test_start__system_v__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0]

    concrete_action_manage_service_instance.start()

    system_v_service = mocked_service_definition.system_v_service_name
    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} start"),
    ]

  def test_start__systemd__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0]

    concrete_action_manage_service_instance.start()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to start the '{service}' service ...\n"
        "INFO - Executing: 'service {system_v_service} start' ...\n"
        "ERROR - Command: 'service {system_v_service} start' failed!\n"
        "WARNING - Service: '{service}' could not be started via a System V "
        "service.\n"
        "INFO - Executing: 'systemctl start {systemd_unit}' ...\n"
        "INFO - Service: done attempting to start the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
        systemd_unit=mocked_service_definition.systemd_unit_name,
    )

  def test_start__systemd__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0]

    concrete_action_manage_service_instance.start()

    system_v_service = mocked_service_definition.system_v_service_name
    systemd_unit = mocked_service_definition.systemd_unit_name
    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} start"),
        mock.call(f"systemctl start {systemd_unit}"),
    ]

  def test_start__process_not_found__logging(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 127]

    concrete_action_manage_service_instance.start()

    assert mocked_stream.getvalue() == (
        "INFO - Service: attempting to start the '{service}' service ...\n"
        "INFO - Executing: 'service {system_v_service} start' ...\n"
        "ERROR - Command: 'service {system_v_service} start' failed!\n"
        "WARNING - Service: '{service}' could not be started via a System V "
        "service.\n"
        "INFO - Executing: 'systemctl start {systemd_unit}' ...\n"
        "ERROR - Command: 'systemctl start {systemd_unit}' failed!\n"
        "WARNING - Service: '{service}' could not be started via a systemd "
        "unit.\n"
        "ERROR - Service: IMPORTANT! The '{service}' service could not be "
        "started!\n"
        "ERROR - Service: Please start it manually!\n"
        "INFO - Service: done attempting to start the '{service}' service.\n"
    ).format(
        service=mocked_service_definition.service_name,
        system_v_service=mocked_service_definition.system_v_service_name,
        systemd_unit=mocked_service_definition.systemd_unit_name,
    )

  def test_start__process_not_found__system_calls(
      self,
      concrete_action_manage_service_instance: ManageServiceAction,
      mocked_service_definition: ServiceDefinition,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 127]

    concrete_action_manage_service_instance.start()

    system_v_service = mocked_service_definition.system_v_service_name
    systemd_unit = mocked_service_definition.systemd_unit_name
    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} start"),
        mock.call(f"systemctl start {systemd_unit}"),
    ]
