"""Motion configuration types."""

from typing import List, Literal

from typing_extensions import TypedDict


class TypeUserConfigCamera(TypedDict):
  """Typed representation of motion configuration."""

  MOTION: "TypeUserConfigCameraMotion"


class TypeUserConfigCameraMotion(TypedDict):
  """Typed representation of motion configuration."""

  AUTHENTICATION: "TypeUserConfigCameraMotionAuthentication"
  CAMERAS: List["TypeUserConfigCameraMotionCamera"]
  DETECTION: "TypeUserConfigCameraMotionDetection"
  MOVIES: "TypeUserConfigCameraMotionMovies"
  SNAPSHOTS: "TypeUserConfigCameraMotionSnapshots"


class TypeUserConfigCameraMotionAuthentication(TypedDict):
  """Typed representation of motion authentication configuration."""

  USERNAME: str
  PASSWORD: str


class TypeUserConfigCameraMotionCamera(TypedDict):
  """Typed representation of motion camera configuration."""

  DEVICE: str
  IMAGE: "TypeUserConfigCameraMotionCameraImage"


class TypeUserConfigCameraMotionCameraImage(TypedDict):
  """Typed representation of motion camera image configuration."""

  FRAME_RATE: int
  WIDTH: int
  HEIGHT: int
  AUTO_BRIGHTNESS: Literal["on", "off"]
  BRIGHTNESS: int
  CONTRAST: int
  SATURATION: int
  HUE: int


class TypeUserConfigCameraMotionDetection(TypedDict):
  """Typed representation of motion detection configuration."""

  THRESHOLD: int
  EVENT_GAP: int


class TypeUserConfigCameraMotionMovies(TypedDict):
  """Typed representation of motion movies configuration."""

  LOCATE_MOTION_MODE: Literal["on", "off"]


class TypeUserConfigCameraMotionSnapshots(TypedDict):
  """Typed representation of motion snapshots configuration."""

  QUALITY: int
