
# bot/database/logging_db.py

import aiosqlite
from .db import LOG_DB


async def log_moderation(
    guild_id: int,
    user_id: int,
    moderator_id: int,
    action: str,
    reason: str | None = None
):
    """Record a moderation action in the database."""

    async with aiosqlite.connect(LOG_DB) as db:
        await db.execute("""
            INSERT INTO moderation_logs
                (guild_id, user_id, moderator_id, action, reason)
            VALUES (?, ?, ?, ?, ?)
        """, (
            guild_id,
            user_id,
            moderator_id,
            action,
            reason
        ))

        await db.commit()


async def get_user_logs(guild_id: int, user_id: int):
    """Retrieve a user's moderation history."""

    async with aiosqlite.connect(LOG_DB) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute("""
            SELECT *
            FROM moderation_logs
            WHERE guild_id = ? AND user_id = ?
            ORDER BY timestamp DESC, id DESC
        """, (guild_id, user_id)) as cursor:
            return await cursor.fetchall()
