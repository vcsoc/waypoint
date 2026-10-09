# Pi with Waypoint and a ChatGPT subscription

`docker-compose.chatgpt.yml` builds Waypoint from the checked-out source and runs PostgreSQL pinned by digest. The gateway listens only on `127.0.0.1:4001`, and PostgreSQL has no published port. This is separate from the default Compose stack

The route is Pi -> Waypoint Responses API -> ChatGPT's subscription backend. It uses ChatGPT subscription limits, not OpenAI API credits. A ChatGPT Pro subscription does not provide an OpenAI API key

## Start the gateway

Run these commands from the repository root. If `.env` already exists, add the required settings there instead of replacing it. Keep the salt key unchanged while retaining the database

```bash
umask 077
(
  set -C
  printf 'WAYPOINT_MASTER_KEY=sk-%s\nWAYPOINT_SALT_KEY=sk-%s\nPOSTGRES_PASSWORD=%s\nUI_USERNAME=admin\nUI_PASSWORD=%s\nWAYPOINT_PORT=4001\n' \
    "$(openssl rand -hex 32)" \
    "$(openssl rand -hex 32)" \
    "$(openssl rand -hex 32)" \
    "$(openssl rand -hex 24)" > .env
)
mkdir -p ../data/waypoint "$HOME/.config/waypoint/chatgpt"
chmod 700 "$HOME/.config/waypoint/chatgpt"
docker compose -f docker-compose.chatgpt.yml up -d --wait
```

PostgreSQL stores its data in `../data/waypoint`, relative to the repository root. For this checkout, that is `/Users/chris/projects/vcsoc/data/waypoint`. The directory must exist before startup. Existing installations using the old named volume need an offline copy of their data before switching mounts

The admin UI is at http://127.0.0.1:4001/ui/. Its username and password are `UI_USERNAME` and `UI_PASSWORD` in your private `.env`. Set `WAYPOINT_PORT` there to use another local port, and update Pi's base URL accordingly

## Sign in to ChatGPT

Use a separate login for Waypoint instead of sharing Pi's or Codex's refresh token. Refresh-token rotation can otherwise break one of the clients. The command below stores an independent credential in a temporary login file, then replaces the gateway credential only after authentication succeeds

```bash
docker compose -f docker-compose.chatgpt.yml run --rm --no-deps \
  -e CHATGPT_AUTH_FILE=login.json --entrypoint python waypoint -c \
  'import os; from pathlib import Path; from waypoint.llms.chatgpt.authenticator import Authenticator; os.umask(0o077); auth = Authenticator(); auth.get_access_token(); Path(auth.auth_file).replace(Path(auth.token_dir) / "auth.json"); print("ChatGPT login saved")'
```

Complete the device login in your own browser using the URL and code printed in your terminal. Never share the device code or paste it into an agent conversation. If OpenAI requires device-code login to be enabled, enable it in your ChatGPT account settings before retrying

The gateway reads `auth.json` for subsequent requests and can refresh this independent login. No container restart is needed. The host directory must stay writable so token refreshes can be saved. Set `CHATGPT_AUTH_HOST_DIR` in `.env` to change its location

A copied access token without a refresh token works only until that token expires. It is sufficient for a smoke test, but does not replace this login step

## Connect Pi

Create a virtual key in the admin UI's Keys page, limited to `gpt-6.1-sol`. Keep the master key for administration rather than using it in Pi

Merge this provider into `~/.pi/agent/models.json`, preserving any existing providers:

```json
{
  "providers": {
    "waypoint-local": {
      "baseUrl": "http://127.0.0.1:4001/v1",
      "api": "openai-responses",
      "models": [
        {
          "id": "gpt-6.1-sol",
          "name": "GPT-6.1 Sol (Waypoint / ChatGPT Pro)",
          "reasoning": true,
          "input": ["text", "image"],
          "contextWindow": 272000,
          "maxTokens": 128000
        }
      ]
    }
  }
}
```

Merge the virtual key into `~/.pi/agent/auth.json`, preserving your existing logins:

```json
{
  "waypoint-local": {
    "type": "api_key",
    "key": "YOUR_MODEL_SCOPED_VIRTUAL_KEY"
  }
}
```

Keep `auth.json` private with `chmod 600 ~/.pi/agent/auth.json`. The model and limits above match the installed Pi catalog used for this setup. When changing models, check the current catalog and update both `docker/chatgpt-config.yaml` and Pi's model configuration

Start a new Pi session:

```bash
pi --model waypoint-local/gpt-6.1-sol
```

For an existing session, open `/model` and choose `waypoint-local/gpt-6.1-sol`. This leaves your existing default model unchanged

## Verify and manage

```bash
curl -fsS http://127.0.0.1:4001/health/liveliness
pi --no-extensions --no-skills --no-prompt-templates --no-mcp \
  --no-context-files --no-tools --no-session \
  --model waypoint-local/gpt-6.1-sol --thinking low \
  --print 'Reply with exactly PI_WAYPOINT_CHATGPT_OK'
docker compose -f docker-compose.chatgpt.yml ps
docker compose -f docker-compose.chatgpt.yml logs --tail 100 waypoint
```

The Pi check should print `PI_WAYPOINT_CHATGPT_OK`. It makes a real model request against your subscription. Gateway cost estimates are not a separate OpenAI API bill

Stop the stack with `docker compose -f docker-compose.chatgpt.yml down`. The database bind mount and host credential directory remain intact, even with `--volumes`. Deleting `../data/waypoint` deletes the database, including its virtual keys
