from pathlib import Path
import aiosqlite

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Directory containing SQLite databases
DATA_DIR = BASE_DIR / "data"

# Logging database path
LOG_DB = DATA_DIR / "logs.db"

# Whitelist database path
WL_DB = DATA_DIR / "whitelist.db"


async def init_db():
    """Initialize the database and create tables if necessary."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(LOG_DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS moderation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER,
                moderator_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                reason TEXT,
                timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.commit()

async def init_db_2():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(WL_DB) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS exempt_roles (
            role_id INTEGER NOT NULL,
            guild_id INTEGER NOT NULL,
            exempt_from TEXT NOT NULL,
            PRIMARY KEY (role_id, guild_id, exempt_from)
            );
            CREATE TABLE IF NOT EXISTS exempt_users (
            user_id INTEGER NULL,
            guild_id INTEGER NOT NULL,
            exempt_from TEXT NOT NULL,
            PRIMARY KEY (user_id, guild_id, exempt_from)
            );
            CREATE TABLE IF NOT EXISTS exempt_channels(
            channel_id INTEGER NULL,
            guild_id INTEGER NOT NULL,
            exempt_from TEXT NOT NULL,
            PRIMARY KEY (channel_id, guild_id, exempt_from)
            )
        """)
        await db.commit()
