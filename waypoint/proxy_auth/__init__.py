"""
Proxy Authentication module for Waypoint SDK.

This module provides OAuth2/JWT token management for authenticating
with Waypoint Proxy or any OAuth2-protected endpoint.

Usage:
    from waypoint.proxy_auth import AzureADCredential, ProxyAuthHandler

    waypoint.proxy_auth = ProxyAuthHandler(
        credential=AzureADCredential(),
        scope="api://my-proxy/.default"
    )
"""

from .credentials import (
    AccessToken,
    AzureADCredential,
    GenericOAuth2Credential,
    ProxyAuthHandler,
    TokenCredential,
)

__all__ = [
    "AccessToken",
    "AzureADCredential",
    "GenericOAuth2Credential",
    "ProxyAuthHandler",
    "TokenCredential",
]
