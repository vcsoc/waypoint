# Changeover progress

Reviewed on 2026-10-09 against the complete operator-provided `changeover.md`

Status: local development prototype. Commercial release blocked. No requirement is marked complete solely because its inherited implementation exists

| Phase | State | Verified evidence | Remaining exit work |
| --- | --- | --- | --- |
| P0 Discovery | In progress | Current upstream SHA and license hashes recorded; initial gap and component review | Complete transitive source/artifact inventory and retain/replace review |
| P1 Foundation | Partial | Separate GitHub repositories; original local licensing app; Keycloak PKCE prototype; personal application admin account | Product renaming compatibility policy, approved build, tenant authorization and versioned migrations |
| P2 Licensing | Partial prototype | CRUD, signed development tokens, renewal/revocation and limited local tests | Standard scoped grants, activation/offline flow, immutable revisions, plans/subscriptions, key rotation, continuity, billing and customer portal |
| P3 Identity/governance | Not accepted | Existing gateway behavior not fully audited | GW-01 through GW-14 requirements and cross-tenant evidence |
| P4 Accounting/policies | Not accepted | Existing gateway behavior not fully audited | GW-15 through GW-31 requirements and concurrency/failure evidence |
| P5 Resources/operations | Not accepted | Existing gateway behavior not fully audited | GW-32 through GW-45 requirements and distribution evidence |
| P6 Changeover | Not started | Existing database preserved during earlier mount move | Migration CLI, dry-run/import/reconciliation/restore/cutover/rollback rehearsals |
| P7 Release | Blocked | No commercial release approval claimed | Full suite, artifact/license/vulnerability scans, SBOM, performance and recovery evidence |

The GitHub repositories were renamed to `vcsoc/waypoint` and private `vcsoc/waypass`. The local directory paths and database mounts were not renamed. This avoids a silent data/mount migration while compatibility policy is decided

The operator account `chris` was created in the existing dedicated application realm with first-login password change. Its temporary credential is saved outside Git with owner-only permissions. No master administration role was assigned. Application realm/client renaming and a separate gateway client still need a migration decision and verification

Existing user changes in `docker/chatgpt-config.yaml`, `.pi/`, `vault/` and `changeover.md` are preserved. The repository-wide auto-lint findings are not attributed to the new account or repo rename. No bulk fix of unrelated Python files is planned

The initial matrices are review ledgers, not a complete license inventory or feature acceptance report. See `review-code_report.mdx` for findings and `feature-matrix.csv` for every LIC/GW requirement
