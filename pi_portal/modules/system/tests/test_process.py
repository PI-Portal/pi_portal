"""Test the Process class."""

import signal
from typing import List, Union
from unittest import mock

import pytest
from .. import process

PROCESS_MODULE = process.__name__


class TestProcess:
  """Test the Process class."""

  mock_pid = mock.mock_open(read_data='1234')
  mock_file_not_found = mock.Mock(side_effect=FileNotFoundError)

  sigterm_attempt = [
      mock.call(1234, 0),
      mock.call(1234, signal.SIGTERM),
  ]
  sigkill_attempt = [
      mock.call(1234, 0),
      mock.call(1234, signal.SIGKILL),
  ]

  def test_initialize__attrs(
      self,
      pid_file_path: str,
      process_instance: process.Process,
  ) -> None:
    assert process_instance.pid_file_path == pid_file_path
    assert process_instance.timeout_counter == 10
    assert process_instance.timeout_interval == 0.1

  @mock.patch(PROCESS_MODULE + '.open', mock_pid)
  @mock.patch('os.kill')
  def test_kill__success_sigterm(
      self,
      m_kill: mock.Mock,
      mocked_sleep: mock.Mock,
      process_instance: process.Process,
  ) -> None:
    m_kill.side_effect = [None, ProcessLookupError]

    process_instance.kill()

    assert m_kill.mock_calls == [
        mock.call(1234, 0),
        mock.call(1234, signal.SIGTERM),
    ]
    mocked_sleep.assert_not_called()

  @mock.patch(PROCESS_MODULE + '.open', mock_file_not_found)
  @mock.patch('os.kill')
  def test_kill__pid_not_running__file_not_found(
      self,
      m_kill: mock.Mock,
      mocked_sleep: mock.Mock,
      process_instance: process.Process,
  ) -> None:
    process_instance.kill()

    m_kill.assert_not_called()
    mocked_sleep.assert_not_called()

  @mock.patch(PROCESS_MODULE + '.open', mock_pid)
  @mock.patch('os.kill')
  def test_kill__pid_not_running__no_process_found(
      self,
      m_kill: mock.Mock,
      mocked_sleep: mock.Mock,
      process_instance: process.Process,
  ) -> None:
    m_kill.side_effect = ProcessLookupError

    process_instance.kill()

    m_kill.assert_called_once_with(1234, 0)
    mocked_sleep.assert_not_called()

  @mock.patch(PROCESS_MODULE + '.open', mock_pid)
  @mock.patch('os.kill')
  def test_kill__fails_to_sigterm__success_sigkill(
      self,
      m_kill: mock.Mock,
      mocked_sleep: mock.Mock,
      process_instance: process.Process,
  ) -> None:
    kill: List[Union[OSError, None]] = [None]

    m_kill.side_effect = \
        kill + kill + kill * (process_instance.timeout_counter + 1) + \
        kill + [ProcessLookupError()]

    process_instance.kill()

    assert m_kill.mock_calls == sum(
        [
            self.sigterm_attempt,
            [mock.call(1234, 0)] * (process_instance.timeout_counter + 1),
            self.sigkill_attempt,
        ],
        [],
    )
    assert mocked_sleep.mock_calls == [
        mock.call(process_instance.timeout_interval)
    ] * 10

  @mock.patch(PROCESS_MODULE + '.open', mock_pid)
  @mock.patch('os.kill')
  def test_kill__fails_to_sigterm__reluctant_sigkill(
      self,
      m_kill: mock.Mock,
      mocked_sleep: mock.Mock,
      process_instance: process.Process,
  ) -> None:
    kill: List[Union[OSError, None]] = [None]

    m_kill.side_effect = \
        kill * (process_instance.timeout_counter + 3) + \
        kill * 3 + [ProcessLookupError()]

    process_instance.kill()

    assert m_kill.mock_calls == sum(
        [
            self.sigterm_attempt,
            [mock.call(1234, 0)] * (process_instance.timeout_counter + 1),
            self.sigkill_attempt,
            [mock.call(1234, 0)] * 2,
        ],
        [],
    )
    assert mocked_sleep.mock_calls == [
        mock.call(process_instance.timeout_interval)
    ] * 11

  @mock.patch(PROCESS_MODULE + '.open', mock_pid)
  @mock.patch('os.kill')
  def test_kill__fails_to_sigterm__fails_to_sigkill(
      self,
      m_kill: mock.Mock,
      mocked_sleep: mock.Mock,
      process_instance: process.Process,
  ) -> None:
    kill: List[Union[OSError, None]] = [None]

    m_kill.side_effect = \
        kill * (process_instance.timeout_counter + 3) + \
        kill * (process_instance.timeout_counter + 3)

    with pytest.raises(process.ProcessNotTerminating):
      process_instance.kill()

    assert m_kill.mock_calls == sum(
        [
            self.sigterm_attempt,
            [mock.call(1234, 0)] * (process_instance.timeout_counter + 1),
            self.sigkill_attempt,
            [mock.call(1234, 0)] * (process_instance.timeout_counter + 1),
        ],
        [],
    )
    assert mocked_sleep.mock_calls == [
        mock.call(process_instance.timeout_interval)
    ] * 20
