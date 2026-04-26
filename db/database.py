import sqlite3
import os
from contextlib import contextmanager

DATABASE = os.path.join(os.path.dirname(__file__), "intake.db")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Section 1: Basics
                name TEXT NOT NULL,
                age TEXT,
                self_or_other TEXT,
                preferred_contact TEXT,

                -- Section 2: General Fit
                support_needs TEXT,
                support_needs_description TEXT,
                social_challenges TEXT,

                -- Section 3: Social Preferences
                comfortable_with TEXT,
                overwhelming_things TEXT,

                -- Section 4: Goals
                goals TEXT,
                primary_focus TEXT,

                -- Section 5: Comfort & Safety
                step_away_important TEXT,
                comfort_helpers TEXT,

                -- Section 6: Logistics
                availability TEXT,

                -- Section 7: Optional
                anything_else TEXT
            );
        """)
        conn.commit()

# Initialize on import
init_db()
