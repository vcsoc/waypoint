import sys

from prisma import Prisma

from waypoint._logging import verbose_logger


async def apply_db_fixes(db: Prisma):
    """
    Do Not Run this in production, only use it as a one-time fix
    """
    verbose_logger.warning(
        "DO NOT run this in Production....Running update_unassigned_teams"
    )
    try:
        sql_query = """
            UPDATE "LiteLLM_SpendLogs"
            SET team_id = (
                SELECT vt.team_id
                FROM "LiteLLM_VerificationToken" vt
                WHERE vt.token = "LiteLLM_SpendLogs".api_key
            )
            WHERE team_id IS NULL
            AND EXISTS (
                SELECT 1
                FROM "LiteLLM_VerificationToken" vt
                WHERE vt.token = "LiteLLM_SpendLogs".api_key
            );
        """
        response = await db.query_raw(sql_query)
        sys.stdout.write(
            " ".join(str(_output_value) for _output_value in ("Updated unassigned teams, Response=%s", response)) + "\n"
        )
    except Exception as e:
        raise Exception(f"Error apply_db_fixes: {e!s}")
