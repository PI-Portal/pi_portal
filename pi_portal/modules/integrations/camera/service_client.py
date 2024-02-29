"""The camera service client."""

from typing import Type

from .bases.client import CameraClientBase
from .motion.client import MotionClient

CameraClient: Type[CameraClientBase] = MotionClient
