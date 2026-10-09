from __future__ import annotations

from waypoint.proxy.management.teams.authz import TeamAccess
from waypoint.proxy.management.users.service import PrismaOrgRoles


def get_team_access() -> TeamAccess:
    from waypoint.proxy.proxy_server import prisma_client, proxy_logging_obj, user_api_key_cache

    return TeamAccess(org_roles=PrismaOrgRoles(prisma_client, user_api_key_cache, proxy_logging_obj))
