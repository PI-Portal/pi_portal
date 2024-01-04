"""Test the ServiceStepBase class."""

from io import StringIO
from unittest import mock

from .. import service_step, system_call_step


class TestServiceStepBase:
  """Test the ServiceStepBase class."""

  def test__initialize__attributes(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
  ) -> None:
    assert isinstance(
        concrete_service_step_instance.service,
        service_step.ServiceDefinition,
    )

  def test__initialize__inheritance(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
  ) -> None:
    assert isinstance(
        concrete_service_step_instance,
        service_step.ServiceStepBase,
    )
    assert isinstance(
        concrete_service_step_instance,
        system_call_step.SystemCallBase,
    )

  def test__initialize__service(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    assert concrete_service_step_instance.service == \
        service_definition_instance
    assert service_definition_instance.service_name == \
        "mock_service"
    assert service_definition_instance.system_v_service_name == \
        "mock_system_v_service"
    assert service_definition_instance.systemd_unit_name == \
        "mock_service_unit"

  def test__disable__logs__system_v(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [0]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name

    concrete_service_step_instance.disable()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to disable the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'update-rc.d {system_v_service} disable' ...\n"
        "test - INFO - "
        f"Service: done attempting to disable the '{service}' service.\n"
    )

  def test__disable__logs__systemd(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 0]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.disable()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to disable the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'update-rc.d {system_v_service} disable' ...\n"
        "test - ERROR - "
        f"Command: 'update-rc.d {system_v_service} disable' failed!\n"
        "test - WARNING - "
        f"Service: unable to disable '{service}' via a System V service.\n"
        "test - INFO - "
        f"Executing: 'systemctl disable {systemd_unit}' ...\n"
        "test - INFO - "
        f"Service: done attempting to disable the '{service}' service.\n"
    )

  def test__disable__logs__process_not_found(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 127]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.disable()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to disable the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'update-rc.d {system_v_service} disable' ...\n"
        "test - ERROR - "
        f"Command: 'update-rc.d {system_v_service} disable' failed!\n"
        "test - WARNING - "
        f"Service: unable to disable '{service}' via a System V service.\n"
        "test - INFO - "
        f"Executing: 'systemctl disable {systemd_unit}' ...\n"
        "test - ERROR - "
        f"Command: 'systemctl disable {systemd_unit}' failed!\n"
        "test - WARNING - "
        f"Service: unable to disable '{service}' via systemd.\n"
        "test - WARNING - "
        f"Service: The '{service}' service could not be disabled!\n"
        "test - WARNING - "
        "Service: This service should be controlled by pi_portal!  "
        "Please disable it manually if required!\n"
    )

  def test__disable__system_calls__system_v(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [0]
    system_v_service = service_definition_instance.system_v_service_name

    concrete_service_step_instance.disable()

    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} disable"),
    ]

  def test__disable__system_calls__systemd(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 0]
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.disable()

    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} disable"),
        mock.call(f"systemctl disable {systemd_unit}"),
    ]

  def test__disable__system_calls__process_not_found(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 127]
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.disable()

    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} disable"),
        mock.call(f"systemctl disable {systemd_unit}"),
    ]

  def test__enable__logs__system_v(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [0]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name

    concrete_service_step_instance.enable()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to enable the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'update-rc.d {system_v_service} enable' ...\n"
        "test - INFO - "
        f"Service: done attempting to enable the '{service}' service.\n"
    )

  def test__enable__logs__systemd(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 0, 0]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.enable()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to enable the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'update-rc.d {system_v_service} enable' ...\n"
        "test - ERROR - "
        f"Command: 'update-rc.d {system_v_service} enable' failed!\n"
        "test - WARNING - "
        f"Service: unable to enable '{service}' via a System V service.\n"
        "test - INFO - "
        f"Executing: 'systemctl enable {systemd_unit}' ...\n"
        "test - INFO - "
        f"Service: done attempting to enable the '{service}' service.\n"
    )

  def test__enable__logs__process_not_found(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 127]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.enable()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to enable the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'update-rc.d {system_v_service} enable' ...\n"
        "test - ERROR - "
        f"Command: 'update-rc.d {system_v_service} enable' failed!\n"
        "test - WARNING - "
        f"Service: unable to enable '{service}' via a System V service.\n"
        "test - INFO - "
        f"Executing: 'systemctl enable {systemd_unit}' ...\n"
        "test - ERROR - "
        f"Command: 'systemctl enable {systemd_unit}' failed!\n"
        "test - WARNING - "
        f"Service: unable to enable '{service}' via systemd.\n"
        "test - ERROR - "
        f"Service: IMPORTANT! The '{service}' service could not be enabled!\n"
        "test - ERROR - "
        "Service: Please enable and start it manually!\n"
    )

  def test__enable__system_calls__system_v(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [0]
    system_v_service = service_definition_instance.system_v_service_name

    concrete_service_step_instance.enable()

    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} enable"),
    ]

  def test__enable__system_calls__systemd(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 0]
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.enable()

    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} enable"),
        mock.call(f"systemctl enable {systemd_unit}"),
    ]

  def test__enable__system_calls__process_not_found(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 127]
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.enable()

    assert mocked_system.mock_calls == [
        mock.call(f"update-rc.d {system_v_service} enable"),
        mock.call(f"systemctl enable {systemd_unit}"),
    ]

  def test__stop__logs__system_v(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [0]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name

    concrete_service_step_instance.stop()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to stop the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'service {system_v_service} stop' ...\n"
        "test - INFO - "
        f"Service: done attempting to stop the '{service}' service.\n"
    )

  def test__stop__logs__systemd(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 0]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.stop()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to stop the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'service {system_v_service} stop' ...\n"
        "test - ERROR - "
        f"Command: 'service {system_v_service} stop' failed!\n"
        "test - WARNING - "
        f"Service: '{service}' is not running via a System V service.\n"
        "test - INFO - "
        f"Executing: 'systemctl stop {systemd_unit}' ...\n"
        "test - INFO - "
        f"Service: done attempting to stop the '{service}' service.\n"
    )

  def test__stop__logs__process_not_found(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 127]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.stop()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to stop the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'service {system_v_service} stop' ...\n"
        "test - ERROR - "
        f"Command: 'service {system_v_service} stop' failed!\n"
        "test - WARNING - "
        f"Service: '{service}' is not running via a System V service.\n"
        "test - INFO - "
        f"Executing: 'systemctl stop {systemd_unit}' ...\n"
        "test - ERROR - "
        f"Command: 'systemctl stop {systemd_unit}' failed!\n"
        "test - WARNING - "
        f"Service: '{service}' is not running via a systemd unit.\n"
        "test - WARNING - "
        f"Service: The '{service}' service does not appear to be running ...\n"
        "test - WARNING - "
        "Service: It could be running via an unknown init system.\n"
        "test - INFO - "
        f"Service: done attempting to stop the '{service}' service.\n"
    )

  def test__stop__system_calls__system_v(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [0]
    system_v_service = service_definition_instance.system_v_service_name

    concrete_service_step_instance.stop()

    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} stop"),
    ]

  def test__stop__system_calls__systemd(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 0]
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.stop()

    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} stop"),
        mock.call(f"systemctl stop {systemd_unit}"),
    ]

  def test__stop__system_calls__process_not_found(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 127]
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.stop()

    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} stop"),
        mock.call(f"systemctl stop {systemd_unit}"),
    ]

  def test__start__logs__system_v(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [0]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name

    concrete_service_step_instance.start()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to start the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'service {system_v_service} start' ...\n"
        "test - INFO - "
        f"Service: done attempting to start the '{service}' service.\n"
    )

  def test__start__logs__systemd(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 0]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.start()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to start the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'service {system_v_service} start' ...\n"
        "test - ERROR - "
        f"Command: 'service {system_v_service} start' failed!\n"
        "test - WARNING - "
        f"Service: '{service}' could not be started via a System V service.\n"
        "test - INFO - "
        f"Executing: 'systemctl start {systemd_unit}' ...\n"
        "test - INFO - "
        f"Service: done attempting to start the '{service}' service.\n"
    )

  def test__start__logs__process_not_found(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 127]
    service = service_definition_instance.service_name
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.start()

    assert mocked_stream.getvalue() == (
        "test - INFO - "
        f"Service: attempting to start the '{service}' service ...\n"
        "test - INFO - "
        f"Executing: 'service {system_v_service} start' ...\n"
        "test - ERROR - "
        f"Command: 'service {system_v_service} start' failed!\n"
        "test - WARNING - "
        f"Service: '{service}' could not be started via a System V service.\n"
        "test - INFO - "
        f"Executing: 'systemctl start {systemd_unit}' ...\n"
        "test - ERROR - "
        f"Command: 'systemctl start {systemd_unit}' failed!\n"
        "test - WARNING - "
        f"Service: '{service}' could not be started via a systemd unit.\n"
        "test - ERROR - "
        f"Service: IMPORTANT! The '{service}' service could not be started!\n"
        "test - ERROR - "
        "Service: Please start it manually!\n"
        "test - INFO - "
        f"Service: done attempting to start the '{service}' service.\n"
    )

  def test__start__system_calls__system_v(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [0]
    system_v_service = service_definition_instance.system_v_service_name

    concrete_service_step_instance.start()

    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} start"),
    ]

  def test__start__system_calls__systemd(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 0]
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.start()

    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} start"),
        mock.call(f"systemctl start {systemd_unit}"),
    ]

  def test__start_system_calls__process_not_found(
      self,
      concrete_service_step_instance: service_step.ServiceStepBase,
      mocked_system: mock.Mock,
      service_definition_instance: service_step.ServiceDefinition,
  ) -> None:
    mocked_system.side_effect = [127, 127]
    system_v_service = service_definition_instance.system_v_service_name
    systemd_unit = service_definition_instance.systemd_unit_name

    concrete_service_step_instance.start()

    assert mocked_system.mock_calls == [
        mock.call(f"service {system_v_service} start"),
        mock.call(f"systemctl start {systemd_unit}"),
    ]
