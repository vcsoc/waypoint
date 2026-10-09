# Waypoint

Waypoint is an AI gateway and Python SDK. It provides OpenAI-compatible APIs, provider routing, virtual keys, budgets, guardrails, and an admin dashboard

[Waypass](https://github.com/vcsoc/waypass) manages the independent licenses used by Waypoint. Its licenses are separate from upstream LiteLLM Enterprise licenses

## Local services

The local gateway runs at http://localhost:4001/ui/. Waypass runs at http://localhost:4010. PostgreSQL data is stored outside the source checkouts in `../data/waypoint` and `../data/waypass/postgres`

Start Waypass from its checkout, then start the gateway from this checkout:

```bash
cd ../waypass
docker compose up -d --build --wait
cd ../waypoint
docker compose -f docker-compose.chatgpt.yml -f docker-compose.licensing.yml up -d --build --wait
```

Both application images are built from the checked-out source. Keep the existing `.env` files, signing keys, database passwords, and salt key when restarting an existing installation. Follow [the local ChatGPT setup guide](docker/CHATGPT.md) for a new gateway installation

## Python and CLI

Use `import waypoint` for the Python SDK. The gateway command is `waypoint`, and the proxy client command is `waypoint-proxy`. Build and install the project with the pinned toolchain and dependency versions in `rust-toolchain.toml`, `pyproject.toml`, and `uv.lock`

Application environment variables use the `WAYPOINT_` prefix. Configure independent licensing with `WAYPOINT_LICENSE`, `WAYPOINT_LICENSE_SERVER_URL`, `WAYPOINT_LICENSE_SERVER_TOKEN`, and `WAYPOINT_LICENSE_PUBLIC_KEY_PATH`

## Compatibility

Legacy `litellm` imports and the `litellm` gateway command remain compatibility aliases. Legacy module imports share the canonical modules and their runtime state. Existing SDK type and function names, HTTP/configuration fields such as `litellm_params`, database identifiers, migration history, and Keycloak identifiers remain stable

Legacy `LITELLM_` environment variables are accepted at startup. An explicitly supplied `WAYPOINT_` value takes precedence, including an empty value. New Waypass licenses use the `waypass` issuer; existing correctly signed `litellmlic` licenses still undergo the same expiry, ownership, and revocation checks

See [the rename compatibility contract](docs/changeover/rename-compatibility.md) for the retained references and validation scope

## Attribution

Original copyright notices and licenses remain intact. The core and bundled components retain their respective license files, including the separate enterprise license. Upstream provider documentation, model metadata, published artifacts, and third-party dependencies retain their original identifiers and links where those identify real external resources
