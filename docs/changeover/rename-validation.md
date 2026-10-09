# Rename validation

Waypoint and Waypass were rebuilt from local source and restarted with their existing PostgreSQL mounts. Both application containers and both database containers are healthy

The gateway page at http://localhost:4001/ui/ returns the title `Waypoint Dashboard`. The licensing page at http://localhost:4010 returns the title `Waypass`

The gateway reports an active enterprise license and exposes the existing configured models. A real Responses API request through the configured `gpt-6.1-sol` route returned `WAYPOINT_RENAME_OK`. The request used an input message array required by the subscription backend

User, key, and model counts in the gateway database match the pre-restart snapshot. User, organisation, and license counts in the licensing database also match. Database identifiers, stored tokens, encryption material, and signing keys were not changed

Installed canonical and legacy SDK imports resolve to the same modules. The freshly compiled native extension loads inside the gateway image. MCP remains available, including the canonical authentication handler and its legacy import alias

Focused Python compatibility, license, health, middleware, lazy-import, parameter-schema, and exception tests passed. The dashboard logo and navigation suite passed 79 tests. All five Waypass platform tests passed, including new and historical signed issuers, invalid signatures, and the existing-realm branding update

The four delta gates passed: strict Ruff, type discipline, test quality, and basedpyright. Their comparisons handle historical source paths rather than treating the renamed package as an empty baseline. No rule ceiling or `ANY_CAPS` value was increased

The standalone repository-wide Ruff count fell from 1,707 to 1,590, with no rule count increasing. These remaining failures are not reported as a clean lint run

The host `make check` bootstrap stopped at the dashboard Node version requirement because the host has Node 22. Dashboard tests and both production builds used the pinned Node 24 Docker image instead. The standalone delta gates were run separately to complete their checks

Private diagnostic logs, environment backups, and database-count snapshots remain in `.git/rename-baseline` and are not committed
