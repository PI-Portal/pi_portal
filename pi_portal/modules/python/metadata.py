"""Compatibility shim for importlib across Python versions."""
# pylint: disable=unused-import
# mypy: allow-redefinition

try:
  from importlib.metadata import version as metadata_version
except ImportError:
  from importlib_metadata import version as metadata_versions
