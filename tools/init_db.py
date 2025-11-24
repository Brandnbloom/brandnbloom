import sqlite3
import pathlib
import argparse
import os
import sys

DEFAULT_DB = os.getenv("BNB_DB_FILE", "bnb.sqlite3")
DEFAULT_SCHEMA = os.getenv("BNB_SCHEMA_PATH", "data/schema.sql")


def load_schema(path: str) -> str:
    """Load and return the SQL schema file."""
    if not pathlib.Path(path).exists():
        print(f"[ERROR] Schema file not found: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def confirm_overwrite(db_path: str):
    """Ask before overwriting an existing DB."""
    if pathlib.Path(db_path).exists():
        ans = input(f"Database '{db_path}' already exists. Overwrite? (y/n): ").strip().lower()
        if ans not in ["y", "yes"]:
            print("Cancelled.")
            sys.exit(0)


def init_sqlite(db_path: str, schema_text: str, verbose=False):
    """Initialize SQLite database with provided schema."""
    if verbose:
        print(f"[INFO] Initializing SQLite DB at: {db_path}")

    # Ensure directory exists
    pathlib.Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        conn = sqlite3.connect(db_path)
        conn.executescript(schema_text)
        conn.commit()
        conn.close()
        print(f"[SUCCESS] Database initialized: {db_path}")
    except Exception as e:
        print(f"[ERROR] Failed to initialize database: {e}")
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Initialize BrandNBloom database with schema.")
    parser.add_argument("--db", type=str, default=DEFAULT_DB, help="Path to SQLite database file")
    parser.add_argument("--schema", type=str, default=DEFAULT_SCHEMA, help="Schema SQL file path")
    parser.add_argument("--force", action="store_true", help="Overwrite DB without asking")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed output")

    return parser.parse_args()


def main():
    args = parse_args()

    db_path = args.db
    schema_path = args.schema

    if not args.force:
        confirm_overwrite(db_path)

    schema_text = load_schema(schema_path)
    if args.verbose:
        print(f"[INFO] Loaded schema from: {schema_path}")

    init_sqlite(db_path, schema_text, args.verbose)


if __name__ == "__main__":
    main()
