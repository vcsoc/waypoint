# What is this?
## If litellm license in env, checks if it's valid
import base64
import json
import os
from datetime import datetime
from typing import TYPE_CHECKING, Final

import httpx
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from pydantic import BaseModel, ConfigDict, StrictBool, TypeAdapter, ValidationError

from waypoint._logging import verbose_proxy_logger
from waypoint.constants import NON_LLM_CONNECTION_TIMEOUT
from waypoint.llms.custom_httpx.http_handler import HTTPHandler

if TYPE_CHECKING:
    from waypoint.proxy._types import EnterpriseLicenseData


AUTO_ROUTER_LICENSE_FEATURE: Final = "auto_router"
LICENSE_ALL_FEATURES: Final = "*"
AUTO_ROUTER_LICENSE_REMEDY: Final = "A Waypoint license with the 'auto_router' feature lifts the limit."
_LICENSE_VERDICT: Final = TypeAdapter(object)


class CustomLicenseVerdict(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    verify: StrictBool


class LicenseCheck:
    """
    - Check if license in env
    - Returns if license is valid
    """

    base_url = "https://license.litellm.ai"

    def __init__(self, http_handler: HTTPHandler | None = None) -> None:
        self.license_str = os.getenv("WAYPOINT_LICENSE", None)
        self.custom_license_server_url = os.getenv("WAYPOINT_LICENSE_SERVER_URL")
        self.custom_license_server_token = os.getenv("WAYPOINT_LICENSE_SERVER_TOKEN")
        self.custom_license_public_key_path = os.getenv("WAYPOINT_LICENSE_PUBLIC_KEY_PATH")
        verbose_proxy_logger.debug("License configured: %s", self.license_str is not None)
        self.http_handler = (
            http_handler if http_handler is not None else HTTPHandler(timeout=NON_LLM_CONNECTION_TIMEOUT)
        )
        self._premium_check_logged = False
        self.public_key: RSAPublicKey | None = None
        self.read_public_key()
        self.airgapped_license_data: EnterpriseLicenseData | None = None

    def read_public_key(self):
        try:
            from cryptography.hazmat.primitives import serialization

            # current dir
            current_dir: Final = os.path.dirname(os.path.realpath(__file__))

            # check if public_key.pem exists
            _path_to_public_key: Final = (
                self.custom_license_public_key_path
                if self.custom_license_server_url and self.custom_license_public_key_path
                else os.path.join(current_dir, "public_key.pem")
            )
            if os.path.exists(_path_to_public_key):
                with open(_path_to_public_key, "rb") as key_file:
                    loaded_key: Final = serialization.load_pem_public_key(key_file.read())
                    self.public_key = loaded_key if isinstance(loaded_key, RSAPublicKey) else None
            else:
                self.public_key = None
        except Exception as e:
            verbose_proxy_logger.error("Error reading public key: %s", e)

    def _verify(self, license_str: str) -> bool:
        verbose_proxy_logger.debug(
            "waypoint.proxy.auth.waypoint_license.py::_verify - Checking license against %s/verify_license",
            self.base_url,
        )
        url: Final = f"{self.base_url}/verify_license/{license_str}"

        response: httpx.Response | None = None
        try:  # don't impact user, if call fails
            num_retries: Final = 3
            for i in range(num_retries):
                try:
                    response = self.http_handler.get(url=url)
                    if response is None:
                        raise Exception("No response from license server")
                    response.raise_for_status()
                except httpx.HTTPStatusError:
                    if i == num_retries - 1:
                        raise

            if response is None:
                raise Exception("No response from license server")

            premium: Final = _LICENSE_VERDICT.validate_python(response.json()["verify"])

            assert isinstance(premium, bool)

            verbose_proxy_logger.debug(
                "waypoint.proxy.auth.waypoint_license.py::_verify - License is premium=%s", premium
            )
            return premium
        except Exception as e:
            verbose_proxy_logger.error(
                "waypoint.proxy.auth.waypoint_license.py::_verify - Unable to verify license via api. "
                "error_type=%s status_code=%s",
                type(e).__name__,
                e.response.status_code if isinstance(e, httpx.HTTPStatusError) else None,
            )
            return False

    def _verify_custom_license(self, license_str: str) -> bool:
        if (
            not self.custom_license_server_url
            or not self.custom_license_server_token
            or not self.custom_license_public_key_path
        ):
            self.airgapped_license_data = None
            return False
        if self.verify_license_without_api_request(self.public_key, license_str) is not True:
            return False
        try:
            response: Final = self.http_handler.client.post(
                url=f"{self.custom_license_server_url.rstrip('/')}/api/verify",
                headers={"Authorization": f"Bearer {self.custom_license_server_token}"},
                json={"license": license_str},
                timeout=5,
                follow_redirects=False,
            )
            response.raise_for_status()
            verdict: Final = CustomLicenseVerdict.model_validate_json(response.content)
            if verdict.verify:
                return True
        except (httpx.HTTPError, ValidationError, ValueError) as exc:
            verbose_proxy_logger.warning("Custom license verification failed: %s", type(exc).__name__)
        self.airgapped_license_data = None
        return False

    def is_premium(self) -> bool:
        """
        1. verify_license_without_api_request: checks if license was generate using private / public key pair
        2. _verify: checks if license is valid calling litellm API. This is the old way we were generating/validating license
        """
        try:
            if not self._premium_check_logged:
                verbose_proxy_logger.debug(
                    "waypoint.proxy.auth.waypoint_license.py::is_premium() - ENTERING 'IS_PREMIUM' - License configured: %s",
                    self.license_str is not None,
                )

            if self.license_str is None:
                self.license_str = os.getenv("WAYPOINT_LICENSE", None)

            if not self._premium_check_logged:
                verbose_proxy_logger.debug(
                    "waypoint.proxy.auth.waypoint_license.py::is_premium() - License configured after refresh: %s",
                    self.license_str is not None,
                )
                self._premium_check_logged = True

            if self.license_str is None:
                self.airgapped_license_data = None
                return False
            if self.custom_license_server_url:
                return self._verify_custom_license(self.license_str)
            elif (
                self.verify_license_without_api_request(public_key=self.public_key, license_key=self.license_str)
                is True
            ) or self._verify(license_str=self.license_str) is True:
                return True
            return False
        except Exception:
            self.airgapped_license_data = None
            return False

    def is_over_limit(self, total_users: int) -> bool:
        """
        Check if the license is over the limit
        """
        if self.airgapped_license_data is None:
            return False
        if "max_users" not in self.airgapped_license_data or not isinstance(
            self.airgapped_license_data["max_users"], int
        ):
            return False
        return total_users > self.airgapped_license_data["max_users"]

    def is_team_count_over_limit(self, team_count: int) -> bool:
        """
        Check if the license is over the limit
        """
        if self.airgapped_license_data is None:
            return False

        _max_teams_in_license: Final[int | None] = self.airgapped_license_data.get("max_teams")
        if "max_teams" not in self.airgapped_license_data or not isinstance(_max_teams_in_license, int):
            return False
        return team_count > _max_teams_in_license

    def grants_feature(self, feature: str) -> bool:
        if self.airgapped_license_data is None:
            return False
        allowed_features: Final = self.airgapped_license_data.get("allowed_features")
        granted: Final = allowed_features if isinstance(allowed_features, list) else (allowed_features,)
        return feature in granted or LICENSE_ALL_FEATURES in granted

    def auto_router_capability_limit(self) -> int | None:
        """
        How many auto-routers may claim each gated classifier or customization capability:
        unlimited (None) only when the signed license lists the auto_router feature or the
        "*" wildcard that grants every feature, otherwise one per capability. A license verified
        through the API carries no feature list, so it does not lift the limit either.
        """
        if self.grants_feature(AUTO_ROUTER_LICENSE_FEATURE):
            return None
        return 1

    def verify_license_without_api_request(self, public_key: RSAPublicKey | None, license_key: str) -> bool:
        try:
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import padding

            from waypoint.proxy._types import EnterpriseLicenseData

            if public_key is None:
                self.airgapped_license_data = None
                return False
            padded_license: Final = license_key + "=" * (-len(license_key) % 4)
            decoded: Final = base64.b64decode(padded_license, validate=True)
            message, signature = decoded.split(b".", 1)

            # Verify the signature
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )

            # Decode and parse the data
            license_data: Final = json.loads(message.decode())

            # Check expiration date
            expiration_date: Final = datetime.strptime(license_data["expiration_date"], "%Y-%m-%d")
            if expiration_date < datetime.now():
                self.airgapped_license_data = None
                return False

            self.airgapped_license_data = EnterpriseLicenseData(**license_data)

            return True

        except Exception as e:
            self.airgapped_license_data = None
            verbose_proxy_logger.debug(
                "waypoint.proxy.auth.waypoint_license.py::verify_license_without_api_request - "
                "Unable to verify license locally. error_type=%s",
                type(e).__name__,
            )
            return False
