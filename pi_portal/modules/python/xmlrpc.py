"""Patched XML-RPC client."""

from xmlrpc import \
    client as patched_client  # pylint: disable=unused-import  # nosec B411

from defusedxml import xmlrpc

# Bandit B411
xmlrpc.monkey_patch()
