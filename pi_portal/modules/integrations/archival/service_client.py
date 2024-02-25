"""The archival service client."""

from typing import Type

from .aws.client import S3BucketClient
from .bases.client import ArchivalClientBase

ArchivalClient: Type[ArchivalClientBase] = S3BucketClient
