"""Utilities for testing the Shortbred ToolResult module."""


def package_payload(payload):
    """Wrap the payload in the way the API will actually receive it."""
    return {'proportions': payload}
