"""
Database backend abstraction: SQLite for local dev, Azure SQL for production.
Selected by DB_BACKEND env var ('sqlite' default, 'azure' for pyodbc).
Both expose fetch_all / fetch_one / execute using '?' placeholders.
"""
import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BACKEND = os.getenv("DB_BACKEND", "sqlite").lower()
SQLITE_PATH = os.getenv("SQLITE_PATH", str(Path(__file__).parent / "supplylens.db"))


def get_connection():
    if BACKEND == "azure":
        import pyodbc
        conn_str = (
            f"DRIVER={{{os.getenv('AZURE_SQL_DRIVER', 'ODBC Driver 18 for SQL Server')}}};"
            f"SERVER={os.getenv('AZURE_SQL_SERVER', 'localhost')};"
            f"DATABASE={os.getenv('AZURE_SQL_DATABASE', 'supplylens')};"
            f"UID={os.getenv('AZURE_SQL_USER', '')};PWD={os.getenv('AZURE_SQL_PASSWORD', '')};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )
        return pyodbc.connect(conn_str)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all(query: str, params: tuple = None) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    result = [dict(r) for r in rows] if BACKEND == "sqlite" else \
        [dict(zip([c[0] for c in cur.description], r)) for r in rows]
    cur.close(); conn.close()
    return result


def fetch_one(query: str, params: tuple = None) -> dict | None:
    rows = fetch_all(query, params)
    return rows[0] if rows else None


def execute_many(query: str, seq: list[tuple]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(query, seq)
    conn.commit()
    cur.close(); conn.close()
