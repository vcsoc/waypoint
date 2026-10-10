# Selective upstream fixes

The reviewed inventory contains 88 commits after `5d207d85ee547bc323d704bc6aaab901aa0be8b6`, through `3ea80696246b79535386ee53c710e103a6b08dc0`. This first batch ports eight security and correctness fixes onto Waypoint's standalone history. No upstream remote, commits, tags, packaging manifests, or license changes were imported

## Applied

MCP caller admission credentials are removed from outbound OAuth, deprecated auth, raw-header, and per-server contexts. The internal `x-litellm-api-key` header cannot be forwarded as an extra header. Authorized passthrough probes use each server's prepared credentials rather than the incoming gateway Authorization header. Distinct provider credentials and the public `MCPServer` export remain compatible. Source: `a4fd58501a9b`

Tiered cache billing preserves an explicitly zero hourly cache-write rate. Missing and null rates retain their fallback behavior. Source: `8a348dafd277`

Custom-host URLs ending in `/v1/messages` use Anthropic passthrough framing, including trailing slashes and query strings. Token-count endpoints are not treated as message streams. Source: `fff86d637686`

Anthropic token counting lifts the leading system-message run into the system parameter, preserves cache control and existing system content, and leaves later system messages in place. Invalid system values remain available for provider validation. Source: `d34ad3528191`

Responses-to-chat prompt-cache support uses the serving provider's catalog entry, including base-model aliases, rather than a colliding OpenAI row. Source: `bbe5595a996c`

Custom request and router pricing matches catalog rows within the serving provider. Waypoint also retains that scope when replaying durable registrations after a catalog reload. Source: `fe1e8d118280`

RDS IAM tokens use the database hostname's region, with independent `AWS_RDS_REGION` and `AWS_RDS_READ_REPLICA_REGION` overrides. Custom hostnames retain the SDK client's region when no override is supplied. Initial client construction also accepts the resolved signing region. Source: `da59afee4482`

The Rust workspace pins `serde_with` to `3.21.0` and has a regenerated lockfile for the serialization advisory fix. Source: `3ebc71be2a46`

## Local validation

All four delta gates pass against `8199874124df7812f8c140d0cdaa1f104fdf191e`. Source Ruff and the test-tree Ruff configuration pass. The serialization package passes `cargo test --locked -p waypoint-llms-types`

The complete pricing, router-isolation, database-token, Anthropic-count, and Responses-transformation modules pass 391 tests. The MCP authentication, tool/header, and REST modules passed 1,071 tests with three unrelated root-path rename cases deselected. Four additional extra-header regressions subsequently pass for aggregate and OpenAPI dispatch

Fourteen targeted regression cases fail against the pre-port implementation, covering cache rates, custom-host stream classification, leading system counting, provider-specific prompt caching, and pricing collisions. A broader exploratory run found unrelated rename inconsistencies in root paths, query fixtures, database URL expectations, and embedded subprocess imports. The entire repository test suite is not claimed clean

These are local checks, not CI or reviewer acceptance. A local proxy answered its liveness endpoint, but live-provider validation of the new code has not been completed

## Deferred

The remaining inventory is not automatically merged. Catalog pricing, retirement dates, and row removals need independent provider validation. SDK and Python/Rust bridge restructuring must preserve Waypoint's packaging and Rust contracts. UI additions, new providers, policy features, and CI/test relocations are separate work

Bedrock reasoning and stop-parameter handling, encrypted reasoning on fallback hops, PDF token estimates, batch-file bookkeeping, provider-metered billing, and streaming-log performance remain candidates for a subsequent targeted review
