from pathlib import Path
import aiosqlite

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Directory containing SQLite databases
DATA_DIR = BASE_DIR / "data"

# Logging database path
LOG_DB = DATA_DIR / "logs.db"


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
