"""Test the LoggingConfiguration class."""

import datetime
import json
import logging
from io import StringIO
from typing import cast

from freezegun import freeze_time
from .fixtures import logger_harness


class TestLogger(logger_harness.LoggingConfigurationTestHarness):
  """Test the setup_logger function."""

  def setUp(self) -> None:
    super().setUp()
    self.logger_name = "test_logger"
    self.file_name = "/var/log/mock.filename.log"
    self.logger = self.logging_configuration.configure(
        self.get_logger(),
        self.file_name,
    )

  def test_logger_handler(self) -> None:
    self.assertEqual(len(self.logger.handlers), 1)
    self.assertIsInstance(self.logger.handlers[0], logging.FileHandler)
    self.assertEqual(
        cast(logging.FileHandler, self.logger.handlers[0]).baseFilename,
        self.file_name
    )

  def test_logger_handler_formatter(self) -> None:
    self.assertEqual(len(self.logger.handlers), 1)
    self.assertIsInstance(self.logger.handlers[0], logging.FileHandler)
    self.assertEqual(
        cast(logging.FileHandler, self.logger.handlers[0]).formatter,
        self.logging_configuration.formatter
    )


class TestFormatter(logger_harness.LoggingConfigurationTestHarness):
  """Test the logger formatter."""

  def setUp(self) -> None:
    super().setUp()
    self.logger_name = "testLogger2"
    self.logger = self.get_logger()
    self.handler = logging.StreamHandler(stream=StringIO())
    self.handler.setFormatter(self.logging_configuration.formatter)
    self.logger.addHandler(self.handler)
    self.test_message = "Test Message"

  @freeze_time("2012-01-14")
  def test_logger_formatter(self) -> None:
    self.logger.error(self.test_message)
    self.assertDictEqual(
        json.loads(
            self.handler.stream.getvalue(),  # type: ignore[attr-defined]
        ),
        {
            "message": self.test_message,
            "levelname": "ERROR",
            "name": self.logger_name,
            "asctime": f"{str(datetime.datetime.utcnow()) + ',000'}",
            "trace_id": self.state.log_uuid,
        },
    )
