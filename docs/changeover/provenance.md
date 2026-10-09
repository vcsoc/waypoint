# Provenance and boundaries

Waypoint is a fork of LiteLLM. The upstream license texts and required copyright notices remain unchanged. GitHub repository naming does not change the licensing of inherited components

Waypass's current FastAPI/PostgreSQL models, CRUD API, React/Vite interface, Keycloak integration and development signing service were authored in this workspace. Its UI follows the visual layout of the existing dashboard. No claim of exclusive ownership over inherited gateway functionality or upstream assets is made

The current gateway license integration modifies root-licensed adapter code but still relies on inherited premium gates and a mixed-license development image. It is a development prototype, not an independent implementation of the premium capabilities in the specification

This review read root and enterprise license texts, external functional specifications, build metadata, and gateway wrappers/authentication outside the enterprise directory. Earlier development inspected gateway premium-gate call paths and UI behavior. This record does not prove implementer isolation from restricted material or a legally sufficient clean-room process. No restricted implementation should be supplied to a generator to author replacements

New implementation dependencies are currently obtained from PyPI/npm and pinned by `uv.lock`, hash-checked requirements and `package-lock.json`. Container bases are pinned in build assets. Approval of these sources is not yet a complete package/asset license audit

Unknown, separately licensed and restricted components remain excluded from commercial release unless their terms and intended use are reviewed and adequate rights are documented. The existing development build does not yet enforce that exclusion

Outstanding owner/legal matters include redistribution rights where needed, trademark/name clearance, customer terms, production signing infrastructure and production third-party credentials. Engineering work must not represent these approvals as complete
