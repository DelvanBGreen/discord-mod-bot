import aiosqlite
from .db import WL_DB
filters = ("word", "link", "spam")


async def exempt_user(guild_id, user_id, exempt_from):
    async with aiosqlite.connect(WL_DB) as db:

        # Check if the user is already exempt from all filters
        async with db.execute("""
            SELECT 1 FROM exempt_users
            WHERE guild_id = ?
            AND user_id = ?
            AND exempt_from = 'all'
        """, (guild_id, user_id)) as cursor:
            if await cursor.fetchone():
                return False

        if exempt_from == "all":
            await db.execute("""
                DELETE FROM exempt_users
                WHERE guild_id = ?
                AND user_id = ?
            """, (guild_id, user_id))

        # Add the exemption
        await db.execute("""
            INSERT OR IGNORE INTO exempt_users
            (user_id, guild_id, exempt_from)
            VALUES (?, ?, ?)
        """, (user_id, guild_id, exempt_from))

        await db.commit()
        return True

async def exempt_role(guild_id, role_id, exempt_from):
    async with aiosqlite.connect(WL_DB) as db:

        # Check if the role is already exempt from all filters
        async with db.execute("""
            SELECT 1 FROM exempt_roles
            WHERE guild_id = ?
            AND role_id = ?
            AND exempt_from = 'all'
        """, (guild_id, role_id)) as cursor:
            if await cursor.fetchone():
                return False

        if exempt_from == "all":
            await db.execute("""
                DELETE FROM exempt_roles
                WHERE guild_id = ?
                AND role_id = ?
            """, (guild_id, role_id))

        # Add the exemption
        await db.execute("""
            INSERT OR IGNORE INTO exempt_roles
            (role_id, guild_id, exempt_from)
            VALUES (?, ?, ?)
        """, (role_id, guild_id, exempt_from))

        await db.commit()
        return True

async def exempt_channel(guild_id, channel_id, exempt_from):
    async with aiosqlite.connect(WL_DB) as db:

        # Check if the channel is already exempt from all filters
        async with db.execute("""
            SELECT 1 FROM exempt_channels
            WHERE guild_id = ?
            AND channel_id = ?
            AND exempt_from = 'all'
        """, (guild_id, channel_id)) as cursor:
            if await cursor.fetchone():
                return False

        if exempt_from == "all":
            await db.execute("""
                DELETE FROM exempt_channels
                WHERE guild_id = ?
                AND channel_id = ?
            """, (guild_id, channel_id))

        # Add the exemption
        await db.execute("""
            INSERT OR IGNORE INTO exempt_channels
            (channel_id, guild_id, exempt_from)
            VALUES (?, ?, ?)
        """, (channel_id, guild_id, exempt_from))

        await db.commit()
        return True

async def is_user_exempt(guild_id, user_id, filter_type):
    async with aiosqlite.connect(WL_DB) as db:
        async with db.execute("""
            SELECT 1 FROM exempt_users
            WHERE guild_id = ?
            AND user_id = ?
            AND exempt_from IN (?, 'all')
            LIMIT 1
        """, (guild_id, user_id, filter_type)) as cursor:
            return await cursor.fetchone() is not None

async def is_role_exempt(guild_id, role_id, filter_type):
    async with aiosqlite.connect(WL_DB) as db:
        async with db.execute("""
            SELECT 1 FROM exempt_roles
            WHERE guild_id = ?
            AND role_id = ?
            AND exempt_from IN (?, 'all')
            LIMIT 1
        """, (guild_id, role_id, filter_type)) as cursor:
            return await cursor.fetchone() is not None

async def has_exempt_role(guild_id, roles, filter_type):
    for role in roles:
        if await is_role_exempt(guild_id, role.id, filter_type):
            return True

    return False

async def is_channel_exempt(guild_id, channel_id, filter_type):
    async with aiosqlite.connect(WL_DB) as db:
        async with db.execute("""
            SELECT 1 FROM exempt_channels
            WHERE guild_id = ?
            AND channel_id = ?
            AND exempt_from IN (?, 'all')
            LIMIT 1
        """, (guild_id, channel_id, filter_type)) as cursor:
            return await cursor.fetchone() is not None

async def remove_user_exemption(guild_id, user_id, exempt_from):


    async with aiosqlite.connect(WL_DB) as db:

        # Check if user has an "all" exemption
        async with db.execute("""
            SELECT 1 FROM exempt_users
            WHERE guild_id = ?
              AND user_id = ?
              AND exempt_from = 'all'
        """, (guild_id, user_id)) as cursor:
            has_all = await cursor.fetchone() is not None

        if has_all and exempt_from != "all":
            # Remove "all"
            await db.execute("""
                DELETE FROM exempt_users
                WHERE guild_id = ?
                  AND user_id = ?
                  AND exempt_from = 'all'
            """, (guild_id, user_id))

            # Add remaining exemptions
            for filter_type in filters:
                if filter_type != exempt_from:
                    await db.execute("""
                        INSERT OR IGNORE INTO exempt_users
                        (user_id, guild_id, exempt_from)
                        VALUES (?, ?, ?)
                    """, (user_id, guild_id, filter_type))

            await db.commit()
            return True

        elif exempt_from == "all":
            # Remove every exemption for this user
            cursor = await db.execute("""
                DELETE FROM exempt_users
                WHERE guild_id = ?
                  AND user_id = ?
            """, (guild_id, user_id))

        else:
            # Remove one specific exemption
            cursor = await db.execute("""
                DELETE FROM exempt_users
                WHERE guild_id = ?
                  AND user_id = ?
                  AND exempt_from = ?
            """, (guild_id, user_id, exempt_from))

        await db.commit()
        return cursor.rowcount > 0

async def remove_role_exemption(guild_id, role_id, exempt_from):

    async with aiosqlite.connect(WL_DB) as db:

        # Check if role has an "all" exemption
        async with db.execute("""
            SELECT 1 FROM exempt_roles
            WHERE guild_id = ?
              AND role_id = ?
              AND exempt_from = 'all'
        """, (guild_id, role_id)) as cursor:
            has_all = await cursor.fetchone() is not None

        if has_all and exempt_from != "all":
            # Remove "all"
            await db.execute("""
                DELETE FROM exempt_roles
                WHERE guild_id = ?
                  AND role_id = ?
                  AND exempt_from = 'all'
            """, (guild_id, role_id))

            # Add remaining exemptions
            for filter_type in filters:
                if filter_type != exempt_from:
                    await db.execute("""
                        INSERT OR IGNORE INTO exempt_roles
                        (role_id, guild_id, exempt_from)
                        VALUES (?, ?, ?)
                    """, (role_id, guild_id, filter_type))

            await db.commit()
            return True

        elif exempt_from == "all":
            # Remove every exemption for this role
            cursor = await db.execute("""
                DELETE FROM exempt_roles
                WHERE guild_id = ?
                  AND role_id = ?
            """, (guild_id, role_id))

        else:
            # Remove one specific exemption
            cursor = await db.execute("""
                DELETE FROM exempt_roles
                WHERE guild_id = ?
                  AND role_id = ?
                  AND exempt_from = ?
            """, (guild_id, role_id, exempt_from))

        await db.commit()
        return cursor.rowcount > 0

async def remove_channel_exemption(guild_id, channel_id, exempt_from):
    

    async with aiosqlite.connect(WL_DB) as db:

        # Check if channel has an "all" exemption
        async with db.execute("""
            SELECT 1 FROM exempt_channels
            WHERE guild_id = ?
              AND channel_id = ?
              AND exempt_from = 'all'
        """, (guild_id, channel_id)) as cursor:
            has_all = await cursor.fetchone() is not None

        if has_all and exempt_from != "all":
            # Remove "all"
            await db.execute("""
                DELETE FROM exempt_channels
                WHERE guild_id = ?
                  AND channel_id = ?
                  AND exempt_from = 'all'
            """, (guild_id, channel_id))

            # Add remaining exemptions
            for filter_type in filters:
                if filter_type != exempt_from:
                    await db.execute("""
                        INSERT OR IGNORE INTO exempt_channels
                        (channel_id, guild_id, exempt_from)
                        VALUES (?, ?, ?)
                    """, (channel_id, guild_id, filter_type))

            await db.commit()
            return True

        elif exempt_from == "all":
            # Remove every exemption for this channel
            cursor = await db.execute("""
                DELETE FROM exempt_channels
                WHERE guild_id = ?
                  AND channel_id = ?
            """, (guild_id, channel_id))

        else:
            # Remove one specific exemption
            cursor = await db.execute("""
                DELETE FROM exempt_channels
                WHERE guild_id = ?
                  AND channel_id = ?
                  AND exempt_from = ?
            """, (guild_id, channel_id, exempt_from))

        await db.commit()
        return cursor.rowcount > 0