"""Test the logger configuration module."""

import datetime
import logging
from io import StringIO
from typing import cast
from unittest import TestCase

from freezegun import freeze_time
from pi_portal.modules import logger


class TestLogger(TestCase):
  """Test the setup_logger function."""

  def setUp(self):
    self.file_name = "/var/log/mock.filename.log"
    self.test_logger = logging.getLogger("testLogger")
    self.logger = logger.setup_logger(self.test_logger, self.file_name)

  def test_logger_handler(self):
    self.assertEqual(len(self.logger.handlers), 1)
    self.assertIsInstance(self.logger.handlers[0], logging.FileHandler)
    self.assertEqual(
        cast(logging.FileHandler, self.logger.handlers[0]).baseFilename,
        self.file_name
    )

  def test_logger_handler_formatter(self):
    self.assertEqual(len(self.logger.handlers), 1)
    self.assertIsInstance(self.logger.handlers[0], logging.FileHandler)
    self.assertEqual(
        cast(logging.FileHandler, self.logger.handlers[0]).formatter,
        logger.LOG_FORMATTER
    )


class TestFormatter(TestCase):
  """Test the logger formatter."""

  def setUp(self):
    self.log = logging.getLogger("testLogger2")
    self.handler = logging.StreamHandler(stream=StringIO())
    self.handler.setFormatter(logger.LOG_FORMATTER)
    self.log.addHandler(self.handler)
    self.test_message = "Test Message"

  @freeze_time("2012-01-14")
  def test_logger_formatter(self):
    self.log.error(self.test_message)
    self.assertEqual(
        self.handler.stream.getvalue(),
        f"{str(datetime.datetime.utcnow()) + ',000'} "
        f"[ {logger.LOG_UUID} ] "
        "[ ERROR ] "
        f"{self.test_message}\n"
    )
