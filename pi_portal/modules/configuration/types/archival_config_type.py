"""Archival configuration types."""

from typing_extensions import TypedDict


class TypeUserConfigArchival(TypedDict):
  """Typed representation of the archival configuration."""

  AWS: "TypeUserConfigArchivalAWS"


class TypeUserConfigArchivalAWS(TypedDict):
  """Typed representation of the AWS archival configuration."""

  AWS_ACCESS_KEY_ID: str
  AWS_SECRET_ACCESS_KEY: str
  AWS_S3_BUCKETS: "TypeUserConfigArchivalAWSBuckets"


class TypeUserConfigArchivalAWSBuckets(TypedDict):
  """Typed representation of the required S3 bucket names."""

  LOGS: str
  VIDEOS: str
