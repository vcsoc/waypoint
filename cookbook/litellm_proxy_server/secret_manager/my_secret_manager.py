"""
Example custom secret manager for Waypoint Proxy.

This is a simple in-memory secret manager for testing purposes.
In production, replace this with your actual secret management system.
"""

import sys

import httpx

from waypoint.integrations.custom_secret_manager import CustomSecretManager


class InMemorySecretManager(CustomSecretManager):
    def __init__(self):
        super().__init__(secret_manager_name="in_memory_secrets")
        # Store your secrets in memory
        sys.stdout.write("INITIALIZING CUSTOM SECRET MANAGER IN MEMORY" + "\n")
        self.secrets = {}
        sys.stdout.write("CUSTOM SECRET MANAGER IN MEMORY INITIALIZED" + "\n")

    async def async_read_secret(
        self,
        secret_name: str,
        optional_params: dict | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> str | None:
        """Read secret asynchronously"""
        sys.stdout.write("READING SECRET ASYNCHRONOUSLY" + "\n")
        sys.stdout.write(" ".join(str(_output_value) for _output_value in ("SECRET NAME: %s", secret_name)) + "\n")
        sys.stdout.write(
            " ".join(str(_output_value) for _output_value in ("SECRET: %s", self.secrets.get(secret_name))) + "\n"
        )
        return self.secrets.get(secret_name)

    def sync_read_secret(
        self,
        secret_name: str,
        optional_params: dict | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> str | None:
        """Read secret synchronously"""
        from waypoint._logging import verbose_proxy_logger

        verbose_proxy_logger.info(
            f"CUSTOM SECRET MANAGER: LOOKING FOR SECRET: {secret_name}"
        )
        value = self.secrets.get(secret_name)
        verbose_proxy_logger.info(f"CUSTOM SECRET MANAGER: READ SECRET: {value}")
        return value

    async def async_write_secret(
        self,
        secret_name: str,
        secret_value: str,
        description: str | None = None,
        optional_params: dict | None = None,
        timeout: float | httpx.Timeout | None = None,
        tags: dict | list | None = None,
    ) -> dict:
        """Write a secret to the in-memory store"""
        self.secrets[secret_name] = secret_value
        sys.stdout.write(" ".join(str(_output_value) for _output_value in ("ALL SECRETS=%s", self.secrets)) + "\n")
        return {
            "status": "success",
            "secret_name": secret_name,
            "description": description,
        }

    async def async_delete_secret(
        self,
        secret_name: str,
        recovery_window_in_days: int | None = 7,
        optional_params: dict | None = None,
        timeout: float | httpx.Timeout | None = None,
    ) -> dict:
        """Delete a secret from the in-memory store"""
        if secret_name in self.secrets:
            del self.secrets[secret_name]
            return {"status": "deleted", "secret_name": secret_name}
        return {"status": "not_found", "secret_name": secret_name}
