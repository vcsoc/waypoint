# Activate a local Waypoint enterprise license

Waypass issues independent licenses for Waypoint, not upstream LiteLLM Enterprise installations. A ChatGPT subscription and a Waypoint enterprise license are separate

This guide describes the currently implemented file-based activation flow. Database-backed activation from the Waypoint UI is not deployed yet; do not look for a License settings screen until that feature is available

All credentials below are placeholders. Never commit a downloaded license, private signing key, verification token, master key, or private environment file

## 1. Sign in to Waypass

Open http://localhost:4010 and sign in through Keycloak as `license-admin`. Find its password under `LICENSING_ADMIN_PASSWORD` in `/home/vcsoc/Projects/waypass/.env`. Keep it private

Waypass administrators need the Keycloak `licensing-admin` role. Signing in to the Keycloak administration console alone does not grant access to Waypass

## 2. Create an active premium owner

Open **Organisations** and click **Create organisation**. Each field has a question-mark button with an explanation and example. Hover over it, focus it with the keyboard, or tap it on a touchscreen. Escape dismisses the tooltip

A sample organisation form looks like this:

```text
Name: Engineering team
Slug: engineering-team
Membership: Premium
Access: Active
```

A slug is a unique, short organisation identifier. Use lowercase letters, numbers and hyphens, start with a letter or number, and keep it within 80 characters. `engineering-team` is valid; `Engineering Team` and `engineering_team` are not

Save the organisation and copy the ID shown in its table row. The license's Organisation ID field takes this ID, not the name or slug

Alternatively, create an individual under **Users**:

```text
Name: Alex Taylor
Email: alex@example.org
Keycloak subject: leave blank unless you need an identity link
Organisation ID: leave blank for an individual owner
Membership: Premium
Access: Active
```

The optional Keycloak subject is that person's immutable Keycloak ID, not their username. An active Standard user can also inherit license eligibility from an active premium organisation

A license must have exactly one owner: an organisation or a user. An organisation license is appropriate for one shared Waypoint instance. Waypass records do not automatically create or synchronize Waypoint users

## 3. Issue the license

Open **Licenses** and click **Create license**. A sample form is:

```text
Name: Development gateway
Organisation ID: select the organisation created in step 2
User ID: leave empty
Edition: Enterprise
Expires at start of UTC date: choose a future date
Features: All features (*)
Maximum users: 100
Maximum teams: 10
```

The expiration date is a UTC date. Access ends at midnight UTC at the beginning of that date, not at the end of your local day. Choose an expiration that covers the full period you need

Features is a searchable multi-select. Click an option to add a pill, then click its small remove icon to remove it. Selected options disappear from the suggestions and return after removal, preventing duplicates. Keyboard users can search, use the arrow keys, and press Enter to select

The current supported license selectors are **All features (`*`)** and **Automatic router (`auto_router`)**. Selecting All features replaces individual selections; selecting an individual feature replaces All features. Existing licenses with other identifiers retain those identifiers as removable pills

Most enterprise capabilities currently follow the gateway's valid enterprise-license status. The `auto_router` identifier separately lifts its router capability limit. Do not assume an arbitrary identifier selectively grants or restricts another capability

Click **Save and download license**. Keep the resulting `<license-id>.license` file private. The Licenses table should show **active**. Standard or Suspended owners cannot receive an active license

## 4. Understand the files

For this machine, the relevant paths are:

```text
/home/vcsoc/Projects/waypass/.env                 private Waypass credentials
/home/vcsoc/Projects/waypass/secrets/private.pem  private issuer signing key
/home/vcsoc/Projects/waypass/secrets/public.pem   public verification key
/home/vcsoc/Projects/waypoint/.env                private gateway and Pi settings
/home/vcsoc/Projects/waypoint/.env.licensing      private license and verifier token
/home/vcsoc/Projects/waypoint/docker-compose.licensing.yml
/home/vcsoc/.config/waypoint/compose.pi.yml       private local model-config overlay
```

Do not copy Waypass's private signing key into Waypoint. Waypoint needs only the corresponding public key and the service verification credential

### Private `.env.licensing` sample

The completed file has two assignments. Replace these placeholders using the downloaded license and Waypass's `VERIFICATION_TOKEN`, not a Keycloak login token:

```dotenv
WAYPOINT_LICENSE_SERVER_TOKEN=REPLACE_WITH_WAYPASS_VERIFICATION_TOKEN
WAYPOINT_LICENSE=REPLACE_WITH_DOWNLOADED_LICENSE_CONTENTS
```

Keep permissions at `600`. The file is ignored by Git. The downloaded license is a long single-line value; do not wrap it across several assignments

### Licensing overlay sample

`docker-compose.licensing.yml` should look like this:

```yaml
services:
  waypoint:
    image: waypoint-licensed:local
    build:
      context: .
      target: runtime
    env_file:
      - .env.licensing
    environment:
      WAYPOINT_LICENSE_SERVER_URL: http://waypass-app-1:4010
      WAYPOINT_LICENSE_PUBLIC_KEY_PATH: /run/licenses/public.pem
    networks:
      - default
      - waypass
    volumes:
      - type: bind
        source: ../waypass/secrets/public.pem
        target: /run/licenses/public.pem
        read_only: true
        bind:
          create_host_path: false

networks:
  waypass:
    external: true
    name: waypass_default
```

The overlay joins Waypass's private Docker network. Its internal address is `http://waypass-app-1:4010`; the browser still uses http://localhost:4010. A host-loopback listener is not reachable through `host.docker.internal` from a Linux bridge container, so do not substitute the browser address here

### Private `.env` addition

Keep the gateway's existing master key, salt key, database password, UI password and Pi settings. Add or replace only `COMPOSE_FILE` with:

```dotenv
COMPOSE_FILE=docker-compose.chatgpt.yml:docker-compose.licensing.yml:/home/vcsoc/.config/waypoint/compose.pi.yml
```

This preserves licensing and Pi configuration when you subsequently run plain `docker compose up`. Explicit `-f` arguments override this setting

The local Pi overlay is specific to this machine. Its current mount-only configuration is:

```yaml
services:
  waypoint:
    volumes:
      - /home/vcsoc/.config/waypoint/gateway.yaml:/app/config.yaml:ro
```

Keep your existing overlay if it has additional settings. Do not replace your generated model configuration or copy credentials into the public repository

## 5. Install or renew privately

The following optional command file installs a downloaded license and refreshes the verification credential without displaying either secret. It preserves other entries in an existing `.env.licensing` and works for initial installation or renewal

Save it outside the repository as `/home/vcsoc/.config/waypoint/install-license.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /home/vcsoc/Projects/waypoint
license_file="${1:?Usage: install-license.sh /path/to/downloaded.license}"
test -s "$license_file"
test -f ../waypass/secrets/public.pem
grep -q '^VERIFICATION_TOKEN=' ../waypass/.env

# Both files contain secrets; keep the temporary file private too.
umask 077
temporary="$(mktemp .env.licensing.XXXXXX)"
trap 'rm -f "$temporary"' EXIT

if test -f .env.licensing; then
  awk '!/^(WAYPOINT_LICENSE|WAYPOINT_LICENSE_SERVER_TOKEN)=/' .env.licensing > "$temporary"
fi

# Copy secrets between files, never through command-line arguments or logs.
awk -F= '$1 == "VERIFICATION_TOKEN" { sub(/^[^=]*=/, ""); print "WAYPOINT_LICENSE_SERVER_TOKEN=" $0 }' \
  ../waypass/.env >> "$temporary"
printf 'WAYPOINT_LICENSE=' >> "$temporary"
tr -d '\r\n' < "$license_file" >> "$temporary"
printf '\n' >> "$temporary"
chmod 600 "$temporary"

# Replace atomically so the gateway never reads a half-written environment file.
mv "$temporary" .env.licensing
trap - EXIT
git check-ignore .env.licensing
```

Run it with the actual download path, not the license value:

```bash
chmod 700 /home/vcsoc/.config/waypoint/install-license.sh
/home/vcsoc/.config/waypoint/install-license.sh "$HOME/Downloads/<license-id>.license"
```

Do not enable shell tracing with `set -x` when handling credentials. Keep the download private too, or remove it after installation if you no longer need a separate copy

## 6. Start Waypoint with licensing

Waypass and its database must be running first. From the Waypoint checkout:

```bash
cd /home/vcsoc/Projects/waypoint

# Include both overlays: licensing trust and this machine's subscription models.
docker compose \
  -f docker-compose.chatgpt.yml \
  -f docker-compose.licensing.yml \
  -f /home/vcsoc/.config/waypoint/compose.pi.yml \
  up -d --build --wait

# Preserve this machine's requested restart policy after recreating the gateway.
docker update --restart always "$(docker compose ps -q waypoint)"
```

Omit the Pi overlay and its `COMPOSE_FILE` entry on an installation without that local file. Do not change the database bind mount, database password or salt key when renewing a license

In this legacy file-based flow, changing `.env.licensing` requires recreating Waypoint. Restarting an existing container alone does not reload environment-file values

## 7. Verify enterprise access

Sign out of Waypoint and sign back in at http://localhost:4001/ui/ so your dashboard session picks up its enterprise status. The account menu should show **Premium**, and licensed settings should be available

For an authenticated backend check, pass the master key to curl over standard input rather than exposing it in process arguments:

```bash
cd /home/vcsoc/Projects/waypoint
set -o pipefail

# Only curl receives the header; the command does not print the credential.
docker compose exec -T waypoint python -c \
  'import json, os; print("header = " + json.dumps("Authorization: Bearer " + os.environ["WAYPOINT_MASTER_KEY"]))' \
  | curl --config - -fsS http://127.0.0.1:4001/health/license
```

An illustrative response for an all-features license is:

```json
{
  "has_license": true,
  "license_type": "enterprise",
  "expiration_date": "YOUR_SELECTED_UTC_DATE",
  "allowed_features": ["*"],
  "limits": {
    "max_users": 100,
    "max_teams": 10
  }
}
```

Your date and limits should match the license you issued, not necessarily this example. The health response contains metadata, not the license token. Also exercise an enterprise-only action you intend to use; metadata alone does not test every feature gate

If activation fails, check the owner's Active/Premium status, future expiration, matching signing/public keys, both private environment fields, and verifier connectivity. This connectivity check needs no credentials:

```bash
docker compose exec waypoint python -c \
  "import urllib.request; print(urllib.request.urlopen('http://waypass-app-1:4010/api/health', timeout=5).read().decode())"
```

A working verifier responds with `{"status":"ok"}`. A missing `waypass_default` network means the Waypass stack must be started first

## 8. Renew, replace or revoke

Under **Licenses**, click **Renew**, choose a future expiration date, and download the replacement token. Editing or renewing invalidates the previous token

Run the private install command with the new download, then recreate Waypoint as in step 6. Do not append another `WAYPOINT_LICENSE` assignment manually; the install command replaces the previous value while preserving unrelated settings

Use **Revoke** to disable a license. Suspending its owner or removing Premium eligibility also disables it. Online verification fails closed if Waypass is unavailable. The running gateway refreshes its enterprise gate on the next request after its 30-second verification cache expires

Back up `/home/vcsoc/data/waypass`, the Waypass signing key and encryption key together. Keep `/home/vcsoc/data/waypoint` and its existing salt key too. Do not rotate or delete these keys casually
