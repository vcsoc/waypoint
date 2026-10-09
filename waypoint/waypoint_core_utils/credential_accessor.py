"""Utils for accessing credentials."""

from typing import Final

import waypoint
from waypoint.types.utils import CredentialItem


class CredentialAccessor:
    @staticmethod
    def find_credential(credential_name: str) -> CredentialItem | None:
        return next(
            (credential for credential in waypoint.credential_list if credential.credential_name == credential_name),
            None,
        )

    @staticmethod
    def get_credential_values(credential_name: str) -> dict:
        """Safe accessor for credentials."""

        credential: Final = CredentialAccessor.find_credential(credential_name)
        return {} if credential is None else credential.credential_values.copy()

    @staticmethod
    def upsert_credentials(credentials: list[CredentialItem]):
        """Add a credential to the list of credentials."""

        credential_names: Final = [cred.credential_name for cred in waypoint.credential_list]

        for credential in credentials:
            if credential.credential_name in credential_names:
                # Find and replace the existing credential in the list
                for i, existing_cred in enumerate(waypoint.credential_list):
                    if existing_cred.credential_name == credential.credential_name:
                        waypoint.credential_list[i] = credential
                        break
            else:
                waypoint.credential_list.append(credential)
