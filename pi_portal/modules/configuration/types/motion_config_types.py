"""Motion configuration types."""

from typing import List, Literal

from typing_extensions import TypedDict


class TypeUserConfigMotion(TypedDict):
  """Typed representation of motion configuration."""

  AUTHENTICATION: "TypeUserConfigMotionAuthentication"
  CAMERAS: List["TypeUserConfigMotionCamera"]
  DETECTION: "TypeUserConfigMotionDetection"
  MOVIES: "TypeUserConfigMotionMovies"
  SNAPSHOTS: "TypeUserConfigMotionSnapshots"


class TypeUserConfigMotionAuthentication(TypedDict):
  """Typed representation of motion authentication configuration."""

  USERNAME: str
  PASSWORD: str


class TypeUserConfigMotionCamera(TypedDict):
  """Typed representation of motion camera configuration."""

  DEVICE: str
  IMAGE: "TypeUserConfigMotionCameraImage"


class TypeUserConfigMotionCameraImage(TypedDict):
  """Typed representation of motion camera image configuration."""

  FRAME_RATE: int
  WIDTH: int
  HEIGHT: int
  AUTO_BRIGHTNESS: Literal["on", "off"]
  BRIGHTNESS: int
  CONTRAST: int
  SATURATION: int
  HUE: int


class TypeUserConfigMotionDetection(TypedDict):
  """Typed representation of motion detection configuration."""

  THRESHOLD: int
  EVENT_GAP: int


class TypeUserConfigMotionMovies(TypedDict):
  """Typed representation of motion movies configuration."""

  LOCATE_MOTION_MODE: Literal["on", "off"]


class TypeUserConfigMotionSnapshots(TypedDict):
  """Typed representation of motion snapshots configuration."""

  QUALITY: int
