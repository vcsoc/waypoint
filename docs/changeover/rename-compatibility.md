# Rename compatibility contract

The gateway application is Waypoint. Its Python distribution and import root are `waypoint`, the Rust workspace is `waypoint-rust`, the optional distributions are `waypoint-enterprise` and `waypoint-proxy-extras`, and the dashboard source is `ui/waypoint-dashboard`

The independent licensing application is Waypass. Both local Compose projects and application images use their new names. The gateway and licensing application are built from local source rather than depending on an upstream gateway image for their application code

## Retained interfaces and data

The `litellm` import root is a compatibility shim for `waypoint`. Historical submodule components also resolve to their canonical counterparts, including imports that combine the new root with an old submodule component. Aliases share module objects, globals, and response types rather than loading a second SDK instance

Existing SDK type names, function names, keyword arguments, provider/callback identifiers, configuration and HTTP fields remain supported. Examples include `litellm_params`, `litellm_version`, and `x-litellm-*` headers. These identify existing interfaces, not a second application

An empty `litellm` distribution adapter in the uv workspace satisfies third-party integrations that still depend on the original distribution name. The canonical wheel supplies the import shim. Upstream dependencies and published upstream artifacts retain their genuine package names and URLs

Application environment variables now use `WAYPOINT_*`. Legacy `LITELLM_*` values populate missing canonical variables at startup, including values loaded from dotenv files. Explicit canonical values take precedence, even when empty. Existing private environment files retain their secret values

Database names, users, Prisma table/model names, SQL identifiers, and historical migration identifiers remain unchanged. Schema and migration SQL are not rewritten as part of the source rename. Existing records continue to use the same identifiers, encryption material, and salt key

Waypass retains the existing Keycloak realm, client, audience, and issuer URLs containing `litellmlic`. Their display names use Waypass. Existing user subjects, roles, redirects, and credentials are preserved

New signed license payloads use the `waypass` issuer. The decoder also accepts the historical `litellmlic` issuer, while continuing to require an authentic signature and the existing database, expiry, ownership, suspension, and revocation checks. No signing keys or existing license tokens are rotated for the rename

Local PostgreSQL mounts remain `../data/waypoint` and `../data/waypass/postgres`. ChatGPT credentials use `$HOME/.config/waypoint/chatgpt`; migrating an existing installation copies the credential file without displaying its contents or changing its permissions

Original copyright and license notices remain intact. External provider documentation, model metadata, historical releases, upstream artifacts, and development branch identifiers retain the original names where changing them would misidentify an external resource or historical record

## Validation scope

Regression coverage checks canonical and legacy module identity, mixed namespace imports, legacy response deserialization, environment precedence, authentic new and legacy license issuers, rejected foreign issuers, and signature tampering. The existing license, health, refresh middleware, lazy-import, parameter-schema, exception-export, and dashboard logo/navigation tests remain part of the validation

Local runtime checks use the existing databases and issued license. They cover healthy application containers, the Waypoint and Waypass page titles, model availability, license verification, and a real request through the gateway. These checks are separate from offline unit tests and builds

The initial repository-wide Ruff baseline contained 1,707 violations. Import and export ordering fixes reduced that count without increasing any rule's count. Remaining pre-existing lint failures are not treated as a passing global lint check
