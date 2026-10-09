Additional files for the proxy. Reduces the size of the main waypoint package.

Currently, only stores the migration.sql files for waypoint-proxy.

To install, run:

```bash
uv add waypoint-proxy-extras
```
OR

```bash
uv tool install 'waypoint[proxy]' # installs waypoint-proxy-extras and other proxy dependencies
```

To use the migrations, run:

```bash
waypoint --use_prisma_migrate
```
