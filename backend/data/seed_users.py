"""Seed the users table with a demo account. Run: python data/seed_users.py"""
import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from auth.security import hash_password  # noqa: E402

DB = Path(__file__).parent.parent / "supplylens.db"
c = sqlite3.connect(DB)
c.executescript("""
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  password_hash TEXT NOT NULL,
  role TEXT DEFAULT 'member',
  tenant_id TEXT DEFAULT 'demo',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
""")
USERS = [
    ("admin@supplylens.io", "Demo Admin", "demo1234", "admin", "demo"),
]
for email, name, pw, role, tenant in USERS:
    c.execute("INSERT OR IGNORE INTO users (email, name, password_hash, role, tenant_id) VALUES (?,?,?,?,?)",
              (email, name, hash_password(pw), role, tenant))
c.commit(); c.close()
print("Seeded users. Login: admin@supplylens.io / demo1234")
