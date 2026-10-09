import os

from waypoint_enterprise.types.proxy.proxy_server import CustomAuthSettings

custom_auth_settings: CustomAuthSettings | None = None


class EnterpriseProxyConfig:
    async def load_custom_auth_settings(self, general_settings: dict) -> CustomAuthSettings | None:
        custom_auth_settings = general_settings.get("custom_auth_settings", None)
        if custom_auth_settings is not None:
            custom_auth_settings = CustomAuthSettings(
                mode=custom_auth_settings.get("mode"),
            )
        return custom_auth_settings

    async def load_enterprise_config(self, general_settings: dict) -> None:
        global custom_auth_settings
        custom_auth_settings = await self.load_custom_auth_settings(general_settings)

    @staticmethod
    def get_custom_docs_description() -> str | None:
        from waypoint.proxy.proxy_server import premium_user

        docs_description: str | None = None
        if premium_user:
            # check if premium_user has custom_docs_description
            docs_description = os.getenv("DOCS_DESCRIPTION")

        return docs_description
