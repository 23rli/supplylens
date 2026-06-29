"""Seed a SQLite parts table with ~120 synthetic parts for local dev. Run: python seed_parts.py"""
import random, sqlite3
from pathlib import Path

random.seed(7)
DB = Path(__file__).parent.parent / "supplylens.db"
VENDORS = [("V1", "Acme Components"), ("V2", "Northwind Parts"), ("V3", "Globex Supply"),
           ("V4", "Initech Hardware"), ("V5", "Umbrella Spares")]
ABC = ["A", "B", "C"]

conn = sqlite3.connect(DB)
conn.executescript(open(Path(__file__).parent / "schema.sql").read())
conn.execute("DELETE FROM parts")
rows = []
for i in range(1, 121):
    v = random.choice(VENDORS)
    lead = random.randint(1, 8)
    forecast = random.randint(520, 20800)
    eoq = random.choice([50, 100, 200, 500])
    ss = random.randint(20, 300)
    rows.append((f"SKU-{i:04d}", f"Part {i}", v[0], v[1], lead, random.choice(ABC),
                 random.randint(0, 2000), random.choice([0, 0, eoq, eoq*2]), forecast,
                 forecast*random.uniform(.8, 1.2), round(random.uniform(.5, 80), 2),
                 random.choice([1, 6, 12, 24]), random.choice([10, 20, 40]), eoq, ss))
conn.executemany("INSERT INTO parts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
conn.commit(); conn.close()
print(f"Seeded {len(rows)} parts into {DB}")
